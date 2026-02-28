export const useAudioRecorder = (tenantId: string) => {
    const socket = ref<WebSocket | null>(null)
    const isRecording = ref(false)
    const mediaRecorder = ref<MediaRecorder | null>(null)
    const audioChunks = ref<Blob[]>([])

    const connect = () => {
        const config = useRuntimeConfig()
        const wsUrl = `${config.public.wsBase}/${tenantId}`

        socket.value = new WebSocket(wsUrl)

        socket.value.onopen = () => {
            console.log('Audio WebSocket connected to', wsUrl)
            socket.value?.send(JSON.stringify({ type: 'ping' }))
        }

        socket.value.onerror = (error) => {
            console.error('WebSocket Error:', error)
        }

        socket.value.onclose = () => {
            console.log('WebSocket closed')
        }
    }

    const audioData = ref<number[]>(new Array(12).fill(10))
    let audioContext: AudioContext | null = null
    let analyser: AnalyserNode | null = null
    let dataArray: Uint8Array | null = null
    let animationFrameId: number | null = null

    const updateVisualizer = () => {
        if (!analyser || !dataArray) return

        analyser.getByteFrequencyData(dataArray)

        // Sample 12 frequency bands
        const step = Math.floor(dataArray.length / 12)
        const newAudioData = []
        for (let i = 0; i < 12; i++) {
            let sum = 0
            for (let j = 0; j < step; j++) {
                sum += dataArray[i * step + j]
            }
            const average = sum / step
            // Map value roughly between 10px and 50px
            const height = Math.max(10, (average / 255) * 50)
            newAudioData.push(height)
        }
        audioData.value = newAudioData

        animationFrameId = requestAnimationFrame(updateVisualizer)
    }

    const startRecording = async () => {
        if (!socket.value || socket.value.readyState !== WebSocket.OPEN) {
            connect()
            // Wait a bit for connection, or ideal is promise
            await new Promise(r => setTimeout(r, 500))
        }

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            mediaRecorder.value = new MediaRecorder(stream)

            // Set up audio visualizer
            audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
            analyser = audioContext.createAnalyser()
            const source = audioContext.createMediaStreamSource(stream)
            source.connect(analyser)

            analyser.fftSize = 64
            const bufferLength = analyser.frequencyBinCount
            dataArray = new Uint8Array(bufferLength)

            updateVisualizer()

            mediaRecorder.value.ondataavailable = (event) => {
                if (event.data.size > 0 && socket.value?.readyState === WebSocket.OPEN) {
                    // Send binary chunk
                    socket.value.send(event.data)
                }
            }

            mediaRecorder.value.start(500) // Send chunk every 500ms
            isRecording.value = true
        } catch (err) {
            console.error('Error starting recording:', err)
        }
    }

    const stopRecording = () => {
        if (mediaRecorder.value && isRecording.value) {
            mediaRecorder.value.stop()
            mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
        }
        if (animationFrameId !== null) {
            cancelAnimationFrame(animationFrameId)
        }
        if (audioContext) {
            audioContext.close()
        }
        // Reset visualizer data
        audioData.value = new Array(12).fill(10)
        isRecording.value = false
    }

    onUnmounted(() => {
        stopRecording()
        if (socket.value) {
            socket.value.close()
        }
    })

    return {
        socket,
        isRecording,
        startRecording,
        stopRecording,
        connect,
        audioData
    }
}

export const useConversationLoop = (tenantId: string) => {
    const { isRecording, startRecording, stopRecording, connect, socket } = useAudioRecorder(tenantId)

    const transcriptions = ref<string[]>([])
    const aiResponses = ref<string[]>([])
    const isProcessing = ref(false)
    const activeTip = ref<any | null>(null)

    // Audio elements for playback
    const audioPlayer = ref<HTMLAudioElement | null>(null)

    watch(socket, (newSocket) => {
        if (!newSocket) return

        newSocket.onmessage = (event) => {
            const data = JSON.parse(event.data)

            if (data.type === 'transcription') {
                transcriptions.value.push(data.text)
                isProcessing.value = true
            }

            if (data.type === 'ai_response') {
                aiResponses.value.push(data.text)
            }

            if (data.type === 'quick_tip') {
                activeTip.value = data.data
            }

            if (data.type === 'audio_response') {
                playAudioResponse(data.audio)
                isProcessing.value = false
            }
        }
    })

    const playAudioResponse = (base64Audio: string) => {
        const audioBlob = b64toBlob(base64Audio, 'audio/mpeg')
        const audioUrl = URL.createObjectURL(audioBlob)

        if (audioPlayer.value) {
            audioPlayer.value.src = audioUrl
            audioPlayer.value.play()
        }
    }

    const b64toBlob = (b64Data: string, contentType = '', sliceSize = 512) => {
        const byteCharacters = atob(b64Data)
        const byteArrays = []

        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize)
            const byteNumbers = new Array(slice.length)
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i)
            }
            const byteArray = new Uint8Array(byteNumbers)
            byteArrays.push(byteArray)
        }

        const blob = new Blob(byteArrays, { type: contentType })
        return blob
    }

    return {
        isRecording,
        isProcessing,
        transcriptions,
        aiResponses,
        activeTip,
        startRecording,
        stopRecording,
        audioPlayer
    }
}

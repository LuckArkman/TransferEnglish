<script setup lang="ts">
const props = defineProps<{
  tenantId: string
}>()

const { 
  isRecording, 
  isProcessing, 
  transcriptions, 
  aiResponses, 
  activeTip,
  activeChallenge,
  startRecording, 
  stopRecording,
  audioPlayer 
} = useConversationLoop(props.tenantId)
</script>

<template>
  <div class="relative w-full max-w-4xl mx-auto">
    <!-- Pressure Mode Indicator -->
    <div v-if="activeChallenge" 
      class="absolute -top-16 left-1/2 -translate-x-1/2 w-full max-w-lg bg-red-600 text-white px-6 py-3 rounded-2xl shadow-2xl animate-bounce flex items-center justify-between z-20"
    >
      <div class="flex items-center gap-3">
        <span class="text-2xl">🔥</span>
        <div>
          <div class="text-[10px] font-bold uppercase tracking-widest opacity-80">Pressure Mode Activated</div>
          <div class="text-sm font-medium">Say: "{{ activeChallenge.target_text }}"</div>
        </div>
      </div>
      <div class="text-xl font-mono font-bold">{{ activeChallenge.time_limit_seconds }}s</div>
    </div>

    <div class="flex flex-col items-center justify-center p-8 bg-slate-800/30 rounded-3xl border border-slate-700 backdrop-blur-xl shadow-2xl"
      :class="{ 'border-red-500/50 shadow-red-500/10': activeChallenge }"
    >
    <!-- Visualizer / Waveform (Placeholder) -->
    <div class="w-full h-48 flex items-center justify-center mb-8 relative">
      <div v-if="isRecording" class="flex items-center gap-1">
        <div v-for="i in 12" :key="i" 
          class="w-1 bg-indigo-500 rounded-full animate-pulse"
          :style="{ height: `${10 + Math.random() * 40}px`, animationDelay: `${i * 100}ms` }">
        </div>
      </div>
      <div v-else-if="isProcessing" class="text-indigo-400 font-medium animate-bounce">
        AI is thinking...
      </div>
      <div v-else class="text-slate-500">
        Click to start conversation
      </div>
    </div>

    <!-- Transcript Area -->
    <div class="w-full max-h-64 overflow-y-auto space-y-4 mb-8 px-4 custom-scrollbar">
      <div v-for="(text, idx) in transcriptions" :key="`t-${idx}`" class="flex flex-col">
        <div class="self-end bg-indigo-600/20 text-indigo-100 px-4 py-2 rounded-2xl rounded-tr-none text-sm max-w-[80%]">
          {{ text }}
        </div>
        <div v-if="aiResponses[idx]" class="self-start bg-slate-700/50 text-slate-100 px-4 py-2 rounded-2xl rounded-tl-none text-sm max-w-[80%] mt-2 border border-slate-600">
          {{ aiResponses[idx] }}
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="flex items-center gap-6">
      <button 
        @mousedown="startRecording" 
        @mouseup="stopRecording"
        @touchstart="startRecording"
        @touchend="stopRecording"
        class="w-20 h-20 rounded-full flex items-center justify-center transition-all shadow-xl group relative"
        :class="isRecording ? 'bg-red-500 shadow-red-500/20 scale-110' : 'bg-indigo-600 hover:bg-indigo-500 shadow-indigo-500/20'"
      >
        <div v-if="isRecording" class="w-6 h-6 bg-white rounded-sm"></div>
        <div v-else class="w-8 h-8 text-white">
          <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>
        </div>
        <!-- Tooltip -->
        <span class="absolute -top-12 left-1/2 -translate-x-1/2 px-3 py-1 bg-slate-900 text-xs text-white rounded-md opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">
          Hold to Speak
        </span>
      </button>
    </div>

    <!-- Hidden audio element for playback -->
    <audio ref="audioPlayer" class="hidden"></audio>
    </div>

    <!-- Quick Feedback Tips -->
    <UiQuickTip v-if="activeTip" :tip="activeTip" @close="activeTip = null" />
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 10px;
}
</style>

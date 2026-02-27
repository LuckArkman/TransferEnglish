<script setup lang="ts">
const props = defineProps<{
  expected: string
  actual: string
}>()

// Simple diff logic for words
const getDiff = computed(() => {
  const expWords = props.expected.toLowerCase().replace(/[.,!?;]/g, '').split(' ')
  const actWords = props.actual.toLowerCase().replace(/[.,!?;]/g, '').split(' ')
  
  return expWords.map(word => {
    const found = actWords.includes(word)
    return {
      text: word,
      status: found ? 'matched' : 'missed'
    }
  })
})
</script>

<template>
  <div class="p-6 bg-slate-800/20 rounded-2xl border border-slate-700/50">
    <h4 class="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Transcription Comparison</h4>
    
    <div class="flex flex-wrap gap-x-2 gap-y-1">
      <span v-for="(word, idx) in getDiff" :key="idx"
        class="text-base transition-colors"
        :class="word.status === 'matched' ? 'text-slate-300' : 'text-rose-500 line-through decoration-2'"
      >
        {{ word.text }}
      </span>
    </div>
    
    <div class="mt-4 pt-4 border-t border-slate-700/30">
      <p class="text-[10px] text-slate-500 italic">
        * Red crossed words were expected but not detected or mispronounced.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Phoneme {
  phoneme: str
  accuracy_score: number
}

interface WordAssessment {
  word: string
  accuracy_score: number
  error_type?: string
  phonemes?: Phoneme[]
}

const props = defineProps<{
  words: WordAssessment[]
}>()

const getWordColor = (score: number) => {
  if (score >= 90) return 'text-emerald-400'
  if (score >= 70) return 'text-amber-400'
  return 'text-rose-400'
}

const getBgColor = (score: number) => {
  if (score >= 90) return 'bg-emerald-500/10 border-emerald-500/30'
  if (score >= 70) return 'bg-amber-500/10 border-amber-500/30'
  return 'bg-rose-500/10 border-rose-500/30'
}
</script>

<template>
  <div class="flex flex-wrap gap-3 p-6 bg-slate-900/50 rounded-2xl border border-slate-800">
    <div v-for="(word, idx) in props.words" :key="idx" 
      class="group relative px-2 py-1 rounded-md border transition-all cursor-help"
      :class="getBgColor(word.accuracy_score)"
    >
      <span class="text-lg font-medium tracking-wide" :class="getWordColor(word.accuracy_score)">
        {{ word.word }}
      </span>
      
      <!-- Tooltip with Phonemes details -->
      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-3 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
        <div class="text-xs text-slate-400 mb-2 flex justify-between">
          <span>Accuracy</span>
          <span :class="getWordColor(word.accuracy_score)">{{ Math.round(word.accuracy_score) }}%</span>
        </div>
        
        <div v-if="word.phonemes && word.phonemes.length" class="flex flex-wrap gap-1">
          <div v-for="(p, pIdx) in word.phonemes" :key="pIdx" 
            class="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-700 text-[10px]"
          >
            <span class="text-slate-300 font-mono">{{ p.phoneme }}</span>
            <div class="w-full h-0.5 bg-slate-700 mt-1 overflow-hidden">
              <div class="h-full" :class="p.accuracy_score >= 80 ? 'bg-emerald-500' : 'bg-rose-500'" :style="{ width: `${p.accuracy_score}%` }"></div>
            </div>
          </div>
        </div>
        
        <div v-if="word.error_type && word.error_type !== 'None'" class="mt-2 text-[10px] text-rose-400 font-bold uppercase">
          {{ word.error_type }}
        </div>
      </div>
    </div>
  </div>
</template>

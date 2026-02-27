<script setup lang="ts">
export interface Tip {
  type: 'grammar' | 'phonetic' | 'info'
  title: string
  message: string
}

const props = defineProps<{
  tip: Tip
}>()

const emit = defineEmits(['close'])

const icons = {
  grammar: '✍️',
  phonetic: '🔊',
  info: '💡'
}

const colors = {
  grammar: 'border-blue-500 bg-blue-500/10 text-blue-200',
  phonetic: 'border-amber-500 bg-amber-500/10 text-amber-200',
  info: 'border-indigo-500 bg-indigo-500/10 text-indigo-200'
}

// Auto-close after 6 seconds
onMounted(() => {
  setTimeout(() => emit('close'), 6000)
})
</script>

<template>
  <div class="fixed bottom-24 right-8 w-80 p-4 rounded-2xl border backdrop-blur-md shadow-2xl animate-in fade-in slide-in-from-right-10 duration-500 group"
    :class="colors[props.tip.type]"
  >
    <div class="flex items-start gap-3">
      <span class="text-xl">{{ icons[props.tip.type] }}</span>
      <div class="flex-1">
        <h5 class="text-sm font-bold uppercase tracking-widest opacity-80 mb-1">
          {{ props.tip.title }}
        </h5>
        <p class="text-xs leading-relaxed">
          {{ props.tip.message }}
        </p>
      </div>
      <button @click="emit('close')" class="opacity-40 hover:opacity-100 transition-opacity">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
    
    <!-- Progress bar for auto-close -->
    <div class="absolute bottom-0 left-0 h-0.5 bg-current opacity-30 animate-shrink" style="animation-duration: 6000ms;"></div>
  </div>
</template>

<style scoped>
@keyframes shrink {
  from { width: 100%; }
  to { width: 0%; }
}
.animate-shrink {
  animation-name: shrink;
  animation-timing-function: linear;
}
</style>

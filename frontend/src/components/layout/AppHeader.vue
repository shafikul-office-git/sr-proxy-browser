<script setup>
import BaseIcon from '../ui/BaseIcon.vue'
import { useTheme } from '../../composables/useTheme'

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  back: { type: Boolean, default: false },
})
defineEmits(['back'])

const { theme, toggle } = useTheme()
</script>

<template>
  <header class="flex flex-wrap items-center gap-3">
    <button v-if="back" type="button" class="icon-btn flex items-center justify-center" aria-label="Back" @click="$emit('back')">
      <BaseIcon name="arrow-left" :size="19" />
    </button>

    <div class="min-w-0 flex-1">
      <h1 class="h1 truncate">{{ title }}</h1>
      <p class="sub truncate">{{ subtitle }}</p>
    </div>

    <div v-if="$slots.default" class="order-last w-full sm:order-none sm:w-auto">
      <slot />
    </div>

    <button
      type="button"
      class="icon-btn flex items-center justify-center"
      :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'"
      :title="theme === 'dark' ? 'Light mode' : 'Dark mode'"
      @click="toggle"
    >
      <BaseIcon :name="theme === 'dark' ? 'sun' : 'moon'" :size="19" />
    </button>
  </header>
</template>

<style scoped>
.h1 { color: var(--text); font-size: 28px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.2; }
.sub { color: var(--muted); font-size: 16px; }
.icon-btn {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  border-radius: 16px;
  border: 1px solid var(--btn-border);
  background: var(--btn-bg);
  color: var(--text);
  cursor: pointer;
  transition: background 0.15s;
}
.icon-btn:hover { background: var(--btn-bg-hover); }
.icon-btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
@media (max-width: 639px) {
  .h1 { font-size: 24px; }
  .sub { font-size: 14px; }
}
</style>

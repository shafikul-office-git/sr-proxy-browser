<script setup>
import BaseIcon from './BaseIcon.vue'

defineProps({
  variant: { type: String, default: 'outline' }, // outline | accent | solid
  size: { type: String, default: 'md' }, // md | sm
  icon: { type: String, default: '' },
  type: { type: String, default: 'button' },
})
</script>

<template>
  <button
    :type="type"
    class="btn inline-flex items-center justify-center gap-2 whitespace-nowrap"
    :class="[`btn--${variant}`, `btn--${size}`]"
  >
    <BaseIcon v-if="icon" :name="icon" :size="18" />
    <slot />
  </button>
</template>

<style scoped>
.btn {
  height: 48px;
  padding: 0 22px;
  border-radius: 16px;
  border: 1px solid var(--btn-border);
  background: var(--btn-bg);
  color: var(--text);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s, transform 0.1s, filter 0.15s, border-color 0.15s;
}
.btn--sm { height: 42px; padding: 0 18px; border-radius: 14px; }
.btn:hover:not(:disabled) { background: var(--btn-bg-hover); }
.btn:active:not(:disabled) { transform: scale(0.98); }
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }

.btn--accent {
  border-color: var(--accent-border);
  background: linear-gradient(90deg, var(--accent-soft), var(--accent2-soft));
}
.btn--accent:hover:not(:disabled) { filter: brightness(1.15); background: linear-gradient(90deg, var(--accent-soft), var(--accent2-soft)); }

.btn--solid {
  border-color: transparent;
  color: #fff;
  background: linear-gradient(90deg, #7c3aed, #06b6d4);
}
.btn--solid:hover:not(:disabled) { filter: brightness(1.1); background: linear-gradient(90deg, #7c3aed, #06b6d4); }
</style>

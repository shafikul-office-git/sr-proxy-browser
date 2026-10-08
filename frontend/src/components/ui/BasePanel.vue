<script setup>
import BaseIcon from './BaseIcon.vue'

defineProps({
  title: { type: String, default: '' },
  icon: { type: String, default: '' },
  tone: { type: String, default: 'cyan' }, // cyan | pink
  padded: { type: Boolean, default: true },
})
</script>

<template>
  <section class="panel relative" :class="padded ? 'p-4 sm:p-6' : ''">
    <h2 v-if="title" class="title mb-4 flex items-center gap-2.5 text-[17px] font-semibold">
      <BaseIcon v-if="icon" :name="icon" :size="18" :class="`icon-${tone}`" />
      {{ title }}
    </h2>
    <slot />
  </section>
</template>

<style scoped>
.panel {
  border-radius: 28px;
  background: var(--panel-bg);
  border: 1px solid var(--panel-border);
  box-shadow: var(--panel-shadow);
  backdrop-filter: blur(18px);
}
.title { color: var(--text); }
.icon-cyan { color: var(--icon-cyan); }
.icon-pink { color: var(--icon-pink); }
</style>

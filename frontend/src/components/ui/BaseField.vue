<script setup>
defineProps({ label: { type: String, required: true } })
</script>

<template>
  <label class="block min-w-0">
    <span class="lbl mb-2 block text-sm">{{ label }}</span>
    <slot />
  </label>
</template>

<style scoped>
.lbl { color: var(--muted); }
</style>

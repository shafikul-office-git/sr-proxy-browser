<script setup>
defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array, required: true }, // [{ value, label }]
})
defineEmits(['update:modelValue'])
</script>

<template>
  <div class="seg grid" :style="{ gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))` }" role="tablist">
    <button
      v-for="o in options"
      :key="o.value"
      type="button"
      role="tab"
      class="item truncate"
      :class="{ active: modelValue === o.value }"
      :aria-selected="modelValue === o.value"
      @click="$emit('update:modelValue', o.value)"
    >
      {{ o.label }}
    </button>
  </div>
</template>

<style scoped>
.seg {
  padding: 5px;
  border-radius: 18px;
  border: 1px solid var(--btn-border);
  background: var(--seg-bg);
}
.item {
  height: 48px;
  padding: 0 8px;
  border: 0;
  border-radius: 14px;
  background: transparent;
  color: var(--muted);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.15s;
}
.item:hover { color: var(--text); }
.item.active {
  color: #fff;
  background: linear-gradient(90deg, #7c3aed, #06b6d4);
  box-shadow: 0 6px 18px -6px rgb(124 58 237 / 0.7);
}
</style>

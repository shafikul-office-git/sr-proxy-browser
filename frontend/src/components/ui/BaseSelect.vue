<script setup>
import { computed } from 'vue'
import BaseIcon from './BaseIcon.vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, required: true }, // ['A', 'B'] or [{ value, label }]
})
defineEmits(['update:modelValue'])

const items = computed(() =>
  props.options.map((o) => (typeof o === 'object' ? o : { value: o, label: o })),
)
</script>

<template>
  <div class="relative min-w-0">
    <select class="field w-full" :value="modelValue" @change="$emit('update:modelValue', $event.target.value)">
      <option v-for="o in items" :key="o.value" :value="o.value">{{ o.label }}</option>
    </select>
    <BaseIcon name="chevron" :size="18" class="chev pointer-events-none absolute right-4 top-1/2 -translate-y-1/2" />
  </div>
</template>

<style scoped>
.field {
  height: 52px;
  padding: 0 44px 0 18px;
  border-radius: 14px;
  border: 1px solid var(--field-border);
  background: var(--field-bg);
  color: var(--text);
  font-size: 16px;
  appearance: none;
  cursor: pointer;
  outline: none;
  text-overflow: ellipsis;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.field:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.chev { color: var(--muted); }
</style>

<script setup>
defineProps({
  modelValue: { type: [String, Number], default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <input
    class="field w-full min-w-0"
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<style scoped>
.field {
  height: 52px;
  padding: 0 18px;
  border-radius: 14px;
  border: 1px solid var(--field-border);
  background: var(--field-bg);
  color: var(--text);
  font-size: 16px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.field::placeholder { color: var(--field-ph); }
.field:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.field:disabled { opacity: 0.5; cursor: not-allowed; }
</style>

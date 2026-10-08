<script setup>
defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  rows: { type: Number, default: 4 },
})
defineEmits(['update:modelValue'])
</script>

<template>
  <textarea
    class="field w-full"
    :rows="rows"
    :value="modelValue"
    :placeholder="placeholder"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<style scoped>
.field {
  padding: 14px 18px;
  border-radius: 14px;
  border: 1px solid var(--field-border);
  background: var(--field-bg);
  color: var(--text);
  font-size: 16px;
  font-family: inherit;
  resize: none;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.field::placeholder { color: var(--field-ph); }
.field:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
</style>

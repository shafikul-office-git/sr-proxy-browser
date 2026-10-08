<script setup>
defineProps({ modelValue: { type: Boolean, default: false }, label: { type: String, default: '' } })
defineEmits(['update:modelValue'])
</script>

<template>
  <button
    type="button"
    role="switch"
    class="track"
    :class="{ on: modelValue }"
    :aria-checked="modelValue"
    :aria-label="label"
    @click="$emit('update:modelValue', !modelValue)"
  >
    <span class="knob" />
  </button>
</template>

<style scoped>
.track {
  position: relative;
  flex-shrink: 0;
  width: 60px;
  height: 36px;
  border: 0;
  border-radius: 999px;
  background: var(--track-off);
  cursor: pointer;
  transition: background 0.2s;
}
.track.on { background: linear-gradient(90deg, #7c3aed, #3b82f6); }
.track:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.knob {
  position: absolute;
  top: 4px;
  left: 4px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 2px 6px rgb(0 0 0 / 0.3);
  transition: transform 0.2s;
}
.on .knob { transform: translateX(24px); }
</style>

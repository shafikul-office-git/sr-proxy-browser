<script setup>
import { ref, watch } from 'vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseIcon from '../ui/BaseIcon.vue'

const props = defineProps({
  proxy: { type: Object, required: true }, // { type, host, port, username, password }
})

const state = ref('idle') // idle | loading | ok | error
const message = ref('')

watch(() => [props.proxy.host, props.proxy.port, props.proxy.type], () => {
  state.value = 'idle'
})

async function check() {
  if (!props.proxy.host || !props.proxy.port) {
    state.value = 'error'
    message.value = 'Enter a host and port first'
    return
  }
  state.value = 'loading'
  // TODO: replace with your real backend call (Electron/Tauri IPC), e.g.
  // const res = await window.api.checkProxy({ ...props.proxy })
  await new Promise((r) => setTimeout(r, 900))
  state.value = 'ok'
  message.value = `Bangladesh, ${Math.floor(90 + Math.random() * 120)} ms`
}
</script>

<template>
  <div class="flex flex-wrap items-center gap-x-4 gap-y-2">
    <BaseButton icon="wifi" class="min-w-[10rem]" :disabled="state === 'loading'" @click="check">
      {{ state === 'loading' ? 'Checking…' : 'Check proxy' }}
    </BaseButton>

    <p v-if="state === 'ok' || state === 'error'" class="result flex items-center gap-1.5 text-[15px] font-medium" :class="state" role="status">
      <BaseIcon :name="state === 'ok' ? 'pin' : 'x'" :size="15" />
      {{ message }}
    </p>
  </div>
</template>

<style scoped>
.result.ok { color: var(--ok); }
.result.error { color: var(--err); }
</style>

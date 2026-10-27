<script setup>
import { ref, watch } from 'vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseIcon from '../ui/BaseIcon.vue'
import {apiCallStore} from '@/stores/api_call'
import { toast } from 'vue3-toastify'

const props = defineProps({
  proxy: { type: Object, required: true }, // { protocol, host, port, username, password }
})

const state = ref('idle') // idle | loading | ok | error
const message = ref('')

watch(() => [props.proxy.host, props.proxy.port, props.proxy.protocol], () => {
  state.value = 'idle'
})

async function check() {
  if (!props.proxy.host || !props.proxy.port) {
    state.value = 'error'
    message.value = 'Enter a host and port first'
    return
  }
  state.value = 'loading'
  const res = await apiCallStore.check_proxy({ ...props.proxy })

  if (res.status >= 200 && res.status < 300){
    if (res.data.status === true){
      state.value = 'ok'
      message.value = `${res.data.message}, ${res.data.response_time_ms} ms`
      toast.success(message.value)
    } else{
      state.value = 'error'
      message.value = res.data.error || res.data.message || 'Proxy check failed'
      toast.error(message.value)
    }
  } else{
    state.value = 'error'
    message.value = apiCallStore.error;
    toast.error(message.value);
  }
  
  // message.value = `Bangladesh, ${Math.floor(90 + Math.random() * 120)} ms`
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

<script setup>
import { reactive, computed } from 'vue'
import BasePanel from '../ui/BasePanel.vue'
import BaseButton from '../ui/BaseButton.vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseSelect from '../ui/BaseSelect.vue'
import ProxyCheck from '../shared/ProxyCheck.vue'

const emit = defineEmits(['launch'])

const proxy = reactive({ protocol: 'HTTP', host: '', port: '', username: '', password: '' })
const canLaunch = computed(() => proxy.host.trim() !== '' && proxy.port !== '')
</script>

<template>
  <BasePanel title="Quick launch with proxy" icon="zap">
    <div class="grid grid-cols-6 gap-3 lg:grid-cols-[8rem_minmax(0,1.5fr)_7rem_minmax(0,1fr)_minmax(0,1fr)]">
      <div class="order-1 col-span-3 lg:order-none lg:col-span-1">
        <BaseSelect v-model="proxy.protocol" :options="['HTTP', 'HTTPS', 'SOCKS5', 'SOCKS4']" />
      </div>
      <div class="order-3 col-span-6 lg:order-none lg:col-span-1">
        <BaseInput v-model="proxy.host" placeholder="123.45.67.89" />
      </div>
      <div class="order-2 col-span-3 lg:order-none lg:col-span-1">
        <BaseInput v-model="proxy.port" type="number" placeholder="8080" />
      </div>
      <div class="order-4 col-span-3 lg:order-none lg:col-span-1">
        <BaseInput v-model="proxy.username" placeholder="Username" />
      </div>
      <div class="order-5 col-span-3 lg:order-none lg:col-span-1">
        <BaseInput v-model="proxy.password" type="password" placeholder="Password" />
      </div>
    </div>

    <div class="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <ProxyCheck :proxy="proxy" />
      <BaseButton icon="rocket" class="sm:min-w-[16rem]" :disabled="!canLaunch" @click="emit('launch', { ...proxy })">
        Launch browser
      </BaseButton>
    </div>
  </BasePanel>
</template>

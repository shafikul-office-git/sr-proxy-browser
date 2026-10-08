<script setup>
import BaseButton from '../ui/BaseButton.vue'
import StatusPill from './StatusPill.vue'

defineProps({ profile: { type: Object, required: true } })
defineEmits(['action'])

const actions = {
  running: { label: 'Close', icon: 'x' },
  stopped: { label: 'Open', icon: 'play' },
  failed: { label: 'Edit', icon: 'pencil' },
}
</script>

<template>
  <li
    class="row grid grid-cols-[auto_minmax(0,1fr)_auto] items-center gap-x-3 gap-y-2 py-4 md:grid-cols-[auto_minmax(0,1.3fr)_minmax(0,1fr)_9rem_8rem] md:gap-x-5"
  >
    <div class="avatar flex items-center justify-center" :style="{ background: profile.gradient }">
      {{ profile.initials }}
    </div>

    <div class="min-w-0">
      <p class="name truncate">{{ profile.name }}</p>
      <p class="env truncate">{{ profile.env }}</p>
    </div>

    <BaseButton
      size="sm"
      class="col-start-3 row-start-1 min-w-[7rem] md:order-last md:col-auto md:row-auto"
      :icon="actions[profile.status].icon"
      @click="$emit('action', profile)"
    >
      {{ actions[profile.status].label }}
    </BaseButton>

    <div class="col-span-2 col-start-2 flex flex-wrap items-center justify-between gap-2 md:contents">
      <span class="proxy truncate">{{ profile.proxy.host }}:{{ profile.proxy.port }}</span>
      <StatusPill :status="profile.status" class="md:justify-self-start" />
    </div>
  </li>
</template>

<style scoped>
.row + .row { border-top: 1px solid var(--divider); }
.avatar {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  color: #fff;
  font-size: 17px;
  font-weight: 700;
  box-shadow: 0 8px 18px -8px rgb(0 0 0 / 0.5);
}
.name { color: var(--text); font-size: 18px; font-weight: 600; }
.env { color: var(--muted); font-size: 15px; }
.proxy { color: var(--muted); font-family: ui-monospace, 'Cascadia Mono', Consolas, monospace; font-size: 14px; }
@media (min-width: 768px) {
  .avatar { width: 64px; height: 64px; border-radius: 18px; font-size: 19px; }
  .name { font-size: 20px; }
  .env { font-size: 17px; }
}
</style>

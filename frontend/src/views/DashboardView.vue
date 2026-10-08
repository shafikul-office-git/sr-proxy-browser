<script setup>
import { ref, computed } from 'vue'
import AppHeader from '../components/layout/AppHeader.vue'
import BaseIcon from '../components/ui/BaseIcon.vue'
import StatCard from '../components/dashboard/StatCard.vue'
import QuickLaunch from '../components/dashboard/QuickLaunch.vue'
import ProfileList from '../components/dashboard/ProfileList.vue'

const props = defineProps({
  profiles: { type: Array, required: true },
  stats: { type: Object, required: true }, // { total, running, working }
})
defineEmits(['new-profile', 'profile-action', 'quick-launch'])

const query = ref('')
const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return props.profiles
  return props.profiles.filter((p) => [p.name, p.env, p.proxy.host].some((v) => v.toLowerCase().includes(q)))
})
</script>

<template>
  <div class="flex flex-col gap-4 sm:gap-5">
    <AppHeader title="SR Proxy Browser" subtitle="Run isolated browsers with their own proxy">
      <label class="relative block">
        <BaseIcon name="search" :size="18" class="s-icon absolute left-4 top-1/2 -translate-y-1/2" />
        <input v-model="query" type="search" placeholder="Search profiles" class="search w-full sm:w-80" />
      </label>
    </AppHeader>

    <div class="grid grid-cols-3 gap-2 sm:gap-4">
      <StatCard icon="users" :value="stats.total" label="Total profiles" tone="violet" />
      <StatCard icon="activity" :value="stats.running" label="Running now" tone="blue" />
      <StatCard icon="shield" :value="stats.working" label="Proxies working" tone="teal" />
    </div>

    <QuickLaunch @launch="$emit('quick-launch', $event)" />

    <ProfileList :profiles="filtered" @new="$emit('new-profile')" @action="$emit('profile-action', $event)" />

    <footer class="foot flex items-center justify-between px-1 pb-1 text-sm">
      <span class="flex items-center gap-1.5"><BaseIcon name="lock" :size="14" /> Saved on this computer only</span>
      <span>v1.0.0</span>
    </footer>
  </div>
</template>

<style scoped>
.s-icon { color: var(--muted); }
.search {
  height: 48px;
  padding: 0 16px 0 46px;
  border-radius: 16px;
  border: 1px solid var(--btn-border);
  background: var(--btn-bg);
  color: var(--text);
  font-size: 16px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.search::placeholder { color: var(--muted); }
.search:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.foot { color: var(--faint); }
</style>

<script setup>
import BaseIcon from '../ui/BaseIcon.vue'

defineProps({ active: { type: String, default: 'profiles' } })
defineEmits(['navigate'])

const items = [
  { id: 'profiles', icon: 'grid', label: 'Profiles' },
  { id: 'proxies', icon: 'globe', label: 'Proxies' },
  { id: 'groups', icon: 'folder', label: 'Groups' },
  { id: 'fingerprints', icon: 'fingerprint', label: 'Fingerprints' },
]
</script>

<template>
  <nav
    class="rail flex shrink-0 items-center gap-2 p-2 sm:m-4 sm:mr-0 sm:w-[78px] sm:flex-col sm:py-4"
    aria-label="Main"
  >
    <div class="logo mr-1 flex items-center justify-center sm:mb-4 sm:mr-0">SR</div>

    <button
      v-for="item in items"
      :key="item.id"
      type="button"
      class="nav flex items-center justify-center"
      :class="{ active: active === item.id }"
      :title="item.label"
      :aria-label="item.label"
      :aria-current="active === item.id ? 'page' : undefined"
      @click="$emit('navigate', item.id)"
    >
      <BaseIcon :name="item.icon" :size="21" />
    </button>

    <div class="flex-1" />

    <button type="button" class="nav flex items-center justify-center" title="Settings" aria-label="Settings">
      <BaseIcon name="settings" :size="21" />
    </button>
  </nav>
</template>

<style scoped>
.rail {
  background: var(--rail-bg);
  border-bottom: 1px solid var(--panel-border);
}
@media (min-width: 640px) {
  .rail {
    border: 1px solid var(--panel-border);
    border-radius: 30px;
  }
}
.logo {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  background: linear-gradient(135deg, #7c3aed, #3b82f6 55%, #06b6d4);
  box-shadow: 0 8px 20px -6px rgb(99 102 241 / 0.7);
}
.nav {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.nav:hover { background: var(--btn-bg-hover); color: var(--text); }
.nav:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.nav.active {
  color: var(--text);
  background: var(--nav-active-bg);
  border-color: var(--nav-active-border);
  box-shadow: 0 0 22px -6px var(--accent);
}
</style>

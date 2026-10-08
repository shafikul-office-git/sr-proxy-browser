<script setup>
import BasePanel from '../ui/BasePanel.vue'
import BaseButton from '../ui/BaseButton.vue'
import ProfileRow from './ProfileRow.vue'

defineProps({ profiles: { type: Array, required: true } })
defineEmits(['new', 'action'])
</script>

<template>
  <BasePanel>
    <div class="head flex items-center justify-between gap-3 pb-4">
      <h2 class="ttl">Your profiles</h2>
      <BaseButton icon="plus" size="sm" @click="$emit('new')">New profile</BaseButton>
    </div>

    <ul v-if="profiles.length" class="list">
      <ProfileRow v-for="p in profiles" :key="p.id" :profile="p" @action="$emit('action', $event)" />
    </ul>
    <p v-else class="empty py-10 text-center">No profiles match your search.</p>
  </BasePanel>
</template>

<style scoped>
.ttl { color: var(--text); font-size: 20px; font-weight: 600; }
.list, .empty { border-top: 1px solid var(--divider); }
.empty { color: var(--muted); }
</style>

<script setup>
import BasePanel from '../ui/BasePanel.vue'
import BaseIcon from '../ui/BaseIcon.vue'

defineProps({
  icon: { type: String, required: true },
  value: { type: [Number, String], required: true },
  label: { type: String, required: true },
  tone: { type: String, default: 'violet' }, // violet | blue | teal
})
</script>

<template>
  <BasePanel :padded="false" class="overflow-hidden">
    <div class="glow pointer-events-none absolute inset-0" :class="`glow-${tone}`" />
    <div class="relative flex flex-col gap-3 p-3 sm:flex-row sm:items-center sm:gap-5 sm:p-6">
      <div class="ibox flex shrink-0 items-center justify-center" :class="`ibox-${tone}`">
        <BaseIcon :name="icon" :size="24" />
      </div>
      <div class="min-w-0">
        <p class="num">{{ value }}</p>
        <p class="lab truncate">{{ label }}</p>
      </div>
    </div>
  </BasePanel>
</template>

<style scoped>
.glow-violet { background: linear-gradient(135deg, rgb(139 92 246 / 0.3), transparent 70%); }
.glow-blue { background: linear-gradient(135deg, rgb(56 189 248 / 0.1), transparent 70%); }
.glow-teal { background: linear-gradient(135deg, rgb(45 212 191 / 0.1), transparent 70%); }

.ibox { width: 44px; height: 44px; border-radius: 16px; }
.ibox-violet { background: rgb(139 92 246 / 0.28); color: #8b5cf6; }
.ibox-blue { background: rgb(14 165 233 / 0.22); color: #0ea5e9; }
.ibox-teal { background: rgb(20 184 166 / 0.22); color: #14b8a6; }

.num { color: var(--text); font-size: 26px; font-weight: 700; line-height: 1.1; }
.lab { color: var(--muted); font-size: 13px; margin-top: 4px; }

@media (min-width: 640px) {
  .ibox { width: 68px; height: 68px; border-radius: 20px; }
  .num { font-size: 36px; }
  .lab { font-size: 17px; }
}
</style>

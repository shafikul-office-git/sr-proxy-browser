<script setup>
defineProps({ status: { type: String, required: true } }) // running | stopped | failed

const labels = { running: 'Running', stopped: 'Stopped', failed: 'Proxy failed' }
</script>

<template>
  <span class="pill inline-flex items-center gap-2 whitespace-nowrap" :class="status">
    <span class="dot" />
    {{ labels[status] }}
  </span>
</template>

<style scoped>
.pill {
  height: 38px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid;
  font-size: 15px;
  font-weight: 500;
}
.dot { width: 9px; height: 9px; border-radius: 50%; background: currentColor; }
.running { color: var(--ok); background: var(--ok-bg); border-color: var(--ok-border); }
.failed { color: var(--err); background: var(--err-bg); border-color: var(--err-border); }
.stopped { color: var(--muted); background: var(--idle-bg); border-color: var(--btn-border); }
</style>

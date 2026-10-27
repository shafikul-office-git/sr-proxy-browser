<script setup>
import { ref, reactive } from 'vue'
import AppSidebar from './components/layout/AppSidebar.vue'
import DashboardView from './views/DashboardView.vue'
import ProfileFormView from './views/ProfileFormView.vue'
import { useTheme } from './composables/useTheme'
import { apiCallStore } from '@/stores/api_call'
import { toast } from 'vue3-toastify'

useTheme() // applies the saved theme (default: dark) before first paint

const view = ref('dashboard') // 'dashboard' | 'form'
const editing = ref(null)
const message = ref('')

// Demo numbers: replace with real data from your backend.
const stats = reactive({ total: 12, running: 3, working: 9 })

const gradients = [
  'linear-gradient(135deg, #7c3aed, #4f46e5)',
  'linear-gradient(135deg, #0ea5e9, #06b6d4)',
  'linear-gradient(135deg, #db2777, #9333ea)',
  'linear-gradient(135deg, #10b981, #0d9488)',
  'linear-gradient(135deg, #f97316, #e11d48)',
]

const profiles = ref([
  { id: 1, name: 'Shop account 01', initials: 'S1', env: 'Chrome 126, Windows', proxy: { type: 'HTTP', host: '192.168.10.21', port: '8080' }, status: 'running', gradient: gradients[0] },
  { id: 2, name: 'Ads profile 02', initials: 'A2', env: 'Chrome 126, Windows', proxy: { type: 'SOCKS5', host: '45.12.88.9', port: '1080' }, status: 'stopped', gradient: gradients[1] },
  { id: 3, name: 'Test US 03', initials: 'T3', env: 'Chrome 125, Windows', proxy: { type: 'HTTP', host: '104.22.7.130', port: '3128' }, status: 'failed', gradient: gradients[2] },
])



function setStatus(profile, status) {
  if (profile.status === 'running') stats.running--
  profile.status = status
  if (status === 'running') stats.running++
}

function addProfile(data, launch) {
  const profile = reactive({
    id: Date.now(),
    status: 'stopped',
    gradient: gradients[profiles.value.length % gradients.length],
    ...data,
  })
  profiles.value.push(profile)
  stats.total++
  if (launch) setStatus(profile, 'running')
}

function onProfileAction(profile) {
  if (profile.status === 'running') setStatus(profile, 'stopped')
  else if (profile.status === 'stopped') setStatus(profile, 'running')
  else openForm(profile) // proxy failed -> edit
}

function openForm(profile = null) {
  editing.value = profile
  view.value = 'form'
}

function closeForm() {
  editing.value = null
  view.value = 'dashboard'
}

function makeInitials(name) {
  const num = name.match(/(\d+)\s*$/)
  const second = num ? num[1].slice(-1) : (name.split(' ')[1]?.[0] ?? '')
  return (name[0] + second).toUpperCase()
}

async function onSubmit({ form, proxy, launch }) {
  const name = form.name.trim() || 'Untitled profile'
  const data = {
    form: {
      ...form, name: name
    },
    initials: makeInitials(name),
    env: `${form.browser}, ${form.os}`,
    proxy: { protocol: proxy.protocol, host: proxy.host || '-', port: proxy.port || '-', username: proxy.username || '', password: proxy.password || '' },
  }

  const res = await apiCallStore.create_browser_profile(data)
  console.log(res)
  if (res.status >= 200 && res.status < 300){
    if (res.data.status === true){
      message.value = `${res.data.message}, ${res.data.response_time_ms} ms`
      toast.success(message.value)
    } else{
      message.value = res.data.error || res.data.message || 'Proxy check failed'
      toast.error(message.value)
    }
  } else{
    message.value = apiCallStore.error;
    toast.error(message.value);
  }

console.log('Submitted profile:', data, 'Launch:', launch)
  if (editing.value) {
    Object.assign(editing.value, data)
    setStatus(editing.value, launch ? 'running' : 'stopped')
  } else {
    addProfile(data, launch)
  }
  // closeForm()
}

function onQuickLaunch(proxy) {
  const name = `Quick session ${profiles.value.length + 1}`
  addProfile(
    { name, initials: makeInitials(name), env: 'Chrome 126, Windows', proxy: { protocol: proxy.protocol, host: proxy.host, port: proxy.port } },
    true,
  )
}


</script>

<template>
  <div class="app h-dvh sm:p-4">
    <div class="shell flex h-full flex-col overflow-hidden sm:flex-row">
      <AppSidebar active="profiles" />

      <main class="scroll-area min-w-0 flex-1 overflow-y-auto p-4 sm:px-5 sm:py-5">
        <div class="mx-auto max-w-5xl">
          <DashboardView
            v-if="view === 'dashboard'"
            :profiles="profiles"
            :stats="stats"
            @new-profile="openForm()"
            @profile-action="onProfileAction"
            @quick-launch="onQuickLaunch"
          />
          <ProfileFormView v-else :key="editing?.id ?? 'new'" :initial="editing" @back="closeForm" @submit="onSubmit" />
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* ---------- Theme tokens: light (default values) ---------- */
:global(:root) {
  color-scheme: light;
  --app-bg: #dedcec;
  --shell-bg:
    radial-gradient(60% 45% at 10% 0%, rgb(139 92 246 / 0.28), transparent 70%),
    radial-gradient(45% 40% at 100% 50%, rgb(236 72 153 / 0.14), transparent 70%),
    radial-gradient(55% 45% at 92% 100%, rgb(20 184 166 / 0.22), transparent 70%),
    #f4f2ff;
  --shell-border: rgb(60 40 120 / 0.15);

  --text: #15122b;
  --muted: #5d5878;
  --faint: #8a85a6;

  --panel-bg: rgb(255 255 255 / 0.72);
  --panel-border: rgb(60 40 120 / 0.12);
  --panel-shadow: 0 14px 34px -18px rgb(76 29 149 / 0.35);
  --rail-bg: rgb(255 255 255 / 0.6);
  --divider: rgb(60 40 120 / 0.12);

  --field-bg: #ffffff;
  --field-border: rgb(60 40 120 / 0.16);
  --field-ph: #9b97b4;

  --btn-bg: rgb(255 255 255 / 0.7);
  --btn-bg-hover: #ffffff;
  --btn-border: rgb(60 40 120 / 0.2);
  --seg-bg: rgb(255 255 255 / 0.6);
  --track-off: rgb(60 40 120 / 0.22);

  --accent: #7c3aed;
  --accent-soft: rgb(124 58 237 / 0.16);
  --accent2-soft: rgb(6 182 212 / 0.2);
  --accent-border: rgb(8 145 178 / 0.55);
  --nav-active-bg: rgb(124 58 237 / 0.14);
  --nav-active-border: rgb(124 58 237 / 0.5);

  --icon-cyan: #0891b2;
  --icon-pink: #db2777;

  --ok: #047857;
  --ok-bg: rgb(16 185 129 / 0.12);
  --ok-border: rgb(16 185 129 / 0.45);
  --err: #be123c;
  --err-bg: rgb(244 63 94 / 0.1);
  --err-border: rgb(244 63 94 / 0.45);
  --idle-bg: rgb(100 100 140 / 0.1);
}

/* ---------- Theme tokens: dark ---------- */
:global(:root.dark) {
  color-scheme: dark;
  --app-bg: #141414;
  --shell-bg:
    radial-gradient(60% 45% at 10% 0%, rgb(124 58 237 / 0.5), transparent 70%),
    radial-gradient(45% 40% at 100% 50%, rgb(190 24 93 / 0.24), transparent 70%),
    radial-gradient(55% 45% at 92% 100%, rgb(20 184 166 / 0.38), transparent 70%),
    #0b0a16;
  --shell-border: rgb(255 255 255 / 0.1);

  --text: #ffffff;
  --muted: rgb(255 255 255 / 0.62);
  --faint: rgb(255 255 255 / 0.45);

  --panel-bg: linear-gradient(135deg, rgb(255 255 255 / 0.075), rgb(255 255 255 / 0.03));
  --panel-border: rgb(255 255 255 / 0.12);
  --panel-shadow: none;
  --rail-bg: rgb(255 255 255 / 0.04);
  --divider: rgb(255 255 255 / 0.12);

  --field-bg: #1b1b1e;
  --field-border: rgb(255 255 255 / 0.08);
  --field-ph: rgb(255 255 255 / 0.38);

  --btn-bg: rgb(255 255 255 / 0.04);
  --btn-bg-hover: rgb(255 255 255 / 0.1);
  --btn-border: rgb(255 255 255 / 0.18);
  --seg-bg: rgb(0 0 0 / 0.25);
  --track-off: rgb(255 255 255 / 0.18);

  --accent: #8b5cf6;
  --accent-soft: rgb(124 58 237 / 0.22);
  --accent2-soft: rgb(6 182 212 / 0.2);
  --accent-border: rgb(34 211 238 / 0.45);
  --nav-active-bg: rgb(124 58 237 / 0.25);
  --nav-active-border: rgb(139 92 246 / 0.6);

  --icon-cyan: #22d3ee;
  --icon-pink: #f43f5e;

  --ok: #34d399;
  --ok-bg: rgb(16 185 129 / 0.12);
  --ok-border: rgb(16 185 129 / 0.45);
  --err: #fb7185;
  --err-bg: rgb(244 63 94 / 0.12);
  --err-border: rgb(244 63 94 / 0.45);
  --idle-bg: rgb(255 255 255 / 0.06);
}

:global(html), :global(body) { margin: 0; background: var(--app-bg); }
:global(*), :global(*::before), :global(*::after) { box-sizing: border-box; }

.app {
  background: var(--app-bg);
  color: var(--text);
  font-family: Inter, 'Segoe UI', system-ui, -apple-system, sans-serif;
  transition: background 0.2s;
}

.shell { background: var(--shell-bg); }
@media (min-width: 640px) {
  .shell { border: 1px solid var(--shell-border); border-radius: 32px; }
}

.scroll-area {
  scrollbar-width: thin;
  scrollbar-color: rgb(148 163 184 / 0.4) transparent;
}
</style>

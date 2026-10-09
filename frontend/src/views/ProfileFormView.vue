<script setup>
import { reactive, computed } from 'vue'
import AppHeader from '../components/layout/AppHeader.vue'
import BasePanel from '../components/ui/BasePanel.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseField from '../components/ui/BaseField.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseSelect from '../components/ui/BaseSelect.vue'
import BaseTextarea from '../components/ui/BaseTextarea.vue'
import BaseIcon from '../components/ui/BaseIcon.vue'
import SegmentedControl from '../components/ui/SegmentedControl.vue'
import ToggleSwitch from '../components/ui/ToggleSwitch.vue'
import ProxyCheck from '../components/shared/ProxyCheck.vue'

const props = defineProps({
  initial: { type: Object, default: null }, // existing profile when editing
})
const emit = defineEmits(['back', 'submit'])

const form = reactive({
  name: props.initial?.name ?? '',
  group: 'No group',
  startPage: 'https://whoer.net/',
  notes: '',
  os: 'Windows 10',
  browser: 'Chrome 126',
  userAgent: 'auto',
  customUserAgent: '',
  screen: '1920 x 1080',
  language: 'Auto from IP',
  timezone: 'Auto from IP',
  webrtc: true,
  canvas: true,
  cookies: true,
})

const proxy = reactive({
  protocol: props.initial?.proxy?.protocol ?? 'HTTP',
  host: props.initial?.proxy?.host ?? '',
  port: props.initial?.proxy?.port ?? '',
  username: '',
  password: '',
})

const hasProxy = computed(() => proxy.protocol !== 'No proxy')

const proxyTypes = ['No proxy', 'HTTP', 'HTTPS', 'SOCKS5', 'SOCKS4'].map((v) => ({ value: v, label: v }))
const groups = ['No group', 'Shop', 'Ads', 'Testing']
const systems = ['Windows 11', 'Windows 10', 'macOS 14', 'Ubuntu 22.04']
const browsers = ['Chrome 126', 'Chrome 125', 'Edge 126', 'Firefox 127']
const userAgents = [
  { value: 'auto', label: 'Auto, matches version' },
  { value: 'custom', label: 'Custom' },
]
const screens = ['1920 x 1080', '1536 x 864', '1366 x 768', '2560 x 1440']
const languages = ['Auto from IP', 'English (US)', 'English (UK)', 'Bangla', 'Spanish']
const timezones = ['Auto from IP', 'Asia/Dhaka', 'America/New_York', 'Europe/London', 'UTC']

const toggles = [
  { key: 'webrtc', title: 'WebRTC protection', hint: 'Hide your real IP' },
  { key: 'canvas', title: 'Canvas noise', hint: 'Unique canvas hash' },
  { key: 'cookies', title: 'Save cookies', hint: 'Keep logins between runs' },
]

function submit(launch) {
  emit('submit', { form: { ...form }, proxy: { ...proxy }, launch })
}
</script>

<template>
  <div class="flex flex-col gap-4 sm:gap-5">
    <AppHeader
      :title="initial ? 'Edit profile' : 'New profile'"
      subtitle="Each profile gets its own isolated browser"
      back
      @back="$emit('back')"
    />

    <div class="grid gap-4 sm:gap-5 lg:grid-cols-2 lg:items-start">
      <div class="flex flex-col gap-4 sm:gap-5">
        <BasePanel title="General" icon="user">
          <div class="flex flex-col gap-4">
            <BaseField label="Profile name">
              <BaseInput v-model="form.name" placeholder="Shop account 04" />
            </BaseField>

            <div class="grid gap-4 sm:grid-cols-2">
              <BaseField label="Group"><BaseSelect v-model="form.group" :options="groups" /></BaseField>
              <BaseField label="Start page">
                <BaseInput v-model="form.startPage" type="url" placeholder="https://whoer.net/" />
              </BaseField>
            </div>

            <BaseField label="Notes">
              <BaseTextarea v-model="form.notes" :rows="4" placeholder="Anything you want to remember" />
            </BaseField>
          </div>
        </BasePanel>

        <BasePanel title="Proxy" icon="globe">
          <div class="flex flex-col gap-3">
            <SegmentedControl v-model="proxy.protocol" :options="proxyTypes" />

            <div class="grid grid-cols-[minmax(0,1fr)_7rem] gap-3">
              <BaseInput v-model="proxy.host" :disabled="!hasProxy" placeholder="123.45.67.89" />
              <BaseInput v-model="proxy.port" :disabled="!hasProxy" type="number" placeholder="8080" />
            </div>
            <div class="grid gap-3 sm:grid-cols-2">
              <BaseInput v-model="proxy.username" :disabled="!hasProxy" placeholder="Username" />
              <BaseInput v-model="proxy.password" :disabled="!hasProxy" type="password" placeholder="Password" />
            </div>

            <ProxyCheck v-if="hasProxy" :proxy="proxy" />
          </div>
        </BasePanel>
      </div>

      <div class="flex flex-col gap-4 sm:gap-5">
        <BasePanel title="Fingerprint" icon="fingerprint" tone="pink">
          <div class="flex flex-col gap-4">
            <div class="grid gap-4 sm:grid-cols-2">
              <BaseField label="Operating system"><BaseSelect v-model="form.os" :options="systems" /></BaseField>
              <BaseField label="Browser version"><BaseSelect v-model="form.browser" :options="browsers" /></BaseField>
            </div>

            <BaseField label="User agent"><BaseSelect v-model="form.userAgent" :options="userAgents" /></BaseField>
            <BaseInput
              v-if="form.userAgent === 'custom'"
              v-model="form.customUserAgent"
              placeholder="Mozilla/5.0 (Windows NT 10.0; Win64; x64) …"
            />

            <div class="grid gap-4 sm:grid-cols-2">
              <BaseField label="Screen size"><BaseSelect v-model="form.screen" :options="screens" /></BaseField>
              <BaseField label="Language"><BaseSelect v-model="form.language" :options="languages" /></BaseField>
            </div>

            <BaseField label="Timezone"><BaseSelect v-model="form.timezone" :options="timezones" /></BaseField>
          </div>
        </BasePanel>

        <BasePanel>
          <ul>
            <li v-for="t in toggles" :key="t.key" class="toggle-row flex items-center justify-between gap-4">
              <div class="min-w-0">
                <p class="t-title">{{ t.title }}</p>
                <p class="t-hint">{{ t.hint }}</p>
              </div>
              <ToggleSwitch v-model="form[t.key]" :label="t.title" />
            </li>
          </ul>
        </BasePanel>
      </div>
    </div>

    <BasePanel>
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <span class="foot flex items-center gap-1.5 text-sm">
          <BaseIcon name="lock" :size="14" /> Saved on this computer only
        </span>
        <div class="grid grid-cols-2 gap-3 sm:flex">
          <BaseButton class="col-span-2 sm:col-auto" @click="$emit('back')">Cancel</BaseButton>
          <BaseButton @click="submit(false)">{{ initial ? 'Save changes' : 'Create profile' }}</BaseButton>
          <BaseButton variant="accent" icon="rocket" @click="submit(true)">
            {{ initial ? 'Save and launch' : 'Create and launch' }}
          </BaseButton>
        </div>
      </div>
    </BasePanel>
  </div>
</template>

<style scoped>
.toggle-row { padding: 14px 0; }
.toggle-row:first-child { padding-top: 0; }
.toggle-row:last-child { padding-bottom: 0; }
.toggle-row + .toggle-row { border-top: 1px solid var(--divider); }
.t-title { color: var(--text); font-size: 17px; font-weight: 500; }
.t-hint { color: var(--muted); font-size: 15px; }
.foot { color: var(--faint); }
</style>

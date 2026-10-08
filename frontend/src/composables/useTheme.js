import { ref, watchEffect } from 'vue'

const KEY = 'sr-theme'
const theme = ref('dark') // the design is dark-first
let ready = false

export function useTheme() {
  if (!ready) {
    ready = true
    try {
      const saved = localStorage.getItem(KEY)
      if (saved === 'light' || saved === 'dark') theme.value = saved
    } catch { /* storage unavailable */ }

    watchEffect(() => {
      document.documentElement.classList.toggle('dark', theme.value === 'dark')
      try { localStorage.setItem(KEY, theme.value) } catch { /* ignore */ }
    })
  }
  const toggle = () => { theme.value = theme.value === 'dark' ? 'light' : 'dark' }
  return { theme, toggle }
}

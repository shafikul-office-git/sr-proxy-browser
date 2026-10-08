<script setup>
import { Sun, Moon } from 'lucide-vue-next'
import { useTheme } from '../composables/useTheme'
import { iconBtn } from '../lib/ui'

const { isDark, toggle } = useTheme()
</script>

<template>
    <button :class="iconBtn" :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'" @click="toggle">
        <Sun v-if="isDark" class="size-5" />
        <Moon v-else class="size-5" />
    </button>
</template>

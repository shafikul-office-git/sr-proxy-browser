<script setup>
import { ArrowLeft } from './icons'
import { iconBtn } from '../lib/ui'

defineProps({
    title: { type: String, required: true },
    subtitle: String,
    back: Boolean,
})

const emit = defineEmits(['back'])
</script>

<template>
    <header class="flex shrink-0 flex-wrap items-center gap-3 px-1">
        <button v-if="back" :class="iconBtn" aria-label="Back" @click="emit('back')">
            <ArrowLeft class="size-5" />
        </button>

        <div class="min-w-0 flex-1 basis-56">
            <h1 class="truncate text-2xl font-semibold tracking-tight">{{ title }}</h1>
            <p v-if="subtitle" class="truncate text-sm text-slate-500 sm:text-base dark:text-white/55">{{ subtitle }}</p>
        </div>

        <div class="flex w-full items-center gap-3 sm:w-auto">
            <slot />
        </div>
    </header>
</template>

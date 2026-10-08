<script setup>
import { ChevronDown } from './icons'
import { field } from '../lib/ui'

defineProps({ modelValue: [String, Number], id: String })
defineEmits(['update:modelValue'])
</script>

<template>
    <div class="relative">
        <select
            :id="id"
            :value="modelValue"
            :class="[field, 'cursor-pointer appearance-none pr-10']"
            @change="$emit('update:modelValue', $event.target.value)"
        >
            <slot />
        </select>
        <ChevronDown class="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-slate-500 dark:text-white/70" />
    </div>
</template>

<script setup>
import Task from './Task.vue'

const props = defineProps({
    tasks: Array,
    readonly: Boolean
})
</script>

<template>
    <div class="divide-y divide-solid divide-gray-300 border border-gray-300">
        <Task v-for="task in tasks" :key="task" 
                :task="task" 
                :readonly="readonly"></Task>
    </div>            
</template>
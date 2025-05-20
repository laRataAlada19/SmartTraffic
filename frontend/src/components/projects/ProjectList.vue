<script setup>
import Project from './Project.vue'

const props = defineProps({
    projects: Array,
    readonly: Boolean
})
</script>

<template>
    <div class="divide-y divide-solid divide-gray-300 border border-gray-300">
        <Project v-for="project in projects" :key="project" 
                :project="project" 
                :readonly="readonly"></Project>
    </div>            
</template>
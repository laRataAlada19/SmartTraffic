<script setup>
import { onMounted } from 'vue'
import ProjectList from './ProjectList.vue'
//import { useProjectStore } from '@/stores/project'
import { useErrorStore } from '@/stores/error'
import { useAuthStore } from '@/stores/auth'

const storeProject = useProjectStore()
const storeError = useErrorStore()
const storeAuth = useAuthStore()

onMounted(() => {
    storeError.resetMessages()
})
</script>

<template>
    <div class="pt-4">
        <RouterLink  v-if="storeAuth.user" :to="{ name: 'createProject'}"  class="mt-4 w-36 h-10 flex items-center justify-center text-sm font-bold rounded-md 
                                    border border-transparent bg-blue-600 text-white 
                                    hover:bg-blue-700 focus:outline-none focus:bg-blue-700">
            New Project
        </RouterLink>        
        <h2 class="pt-8 pb-2 text-2xl">
            Projects
            <span class="text-base">(Total = {{ storeProject.totalProjects }})</span> 
        </h2>
        <div v-show="storeProject.totalProjects > 0">
            <ProjectList :readonly="!storeAuth.user" :projects="storeProject.projects"></ProjectList>
        </div>
    </div>
</template>
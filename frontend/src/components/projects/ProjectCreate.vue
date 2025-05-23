<script setup>
import { ref } from 'vue'
import {useRouter} from 'vue-router'
import ProjectForm from './ProjectForm.vue'
//import { useProjectStore } from '@/stores/project'
import { useErrorStore } from '@/stores/error'

const storeProject = useProjectStore()
const storeError = useErrorStore()

const router = useRouter()

const project = ref({
    id: 0,
    name: ''
})

const create = async (project) => {
    if (await storeProject.insertProject(project)) {        
        router.push({name: 'projects'})
    } 
}

const cancel = () => {
    storeError.resetMessages()
    router.back()
}
</script>

<template>
    <ProjectForm :project="project" title="Create new project" @save="create" @cancel="cancel"></ProjectForm>
</template>
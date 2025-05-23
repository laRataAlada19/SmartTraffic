<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import ProjectForm from './ProjectForm.vue'
//import { useProjectStore } from '@/stores/project'
import { useErrorStore } from '@/stores/error'

const storeProject = useProjectStore()
const storeError = useErrorStore()

const router = useRouter()

const project = ref(null)

const props = defineProps({
    id: {
        type: Number,
        required: true
    }
})

// When the "id" prop changes, the "project" will be loaded from the API
watch(
    () => props.id,
    async (newIDValue) => {
        project.value = await storeProject.fetchProject(newIDValue)
    },
    { immediate: true }
)

const save = async (project) => {
    if (await storeProject.updateProject(project)) {        
        router.push({name: 'projects'})
    }
}

const cancel = () => {
    storeError.resetMessages()
    router.back()
}
</script>

<template>
    <ProjectForm v-if="project" :project="project" :title="`Update project # ${project.id}`" @save="save" @cancel="cancel"></ProjectForm>
</template>
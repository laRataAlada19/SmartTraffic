import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useErrorStore } from '@/stores/error'
import { useRouter } from 'vue-router'
import { useToast } from '@/components/ui/toast/use-toast'
import { ToastAction } from '@/components/ui/toast'
import { h } from 'vue'

export const useProjectStore = defineStore('project', () => {
    const router = useRouter()
    const { toast } = useToast()
    const storeError = useErrorStore()

    const projects = ref([])
    
    const totalProjects = computed(() => {
        return projects.value ? projects.value.length : 0
    })

    const listProjectsIncludingNull = computed(() => [null].concat(projects.value))

    const listProjectsToFilter = computed(() => [
                null,
                {
                    'id': -1,
                    'filterDescription': '-- No project --'
                }
            ].concat(projects.value.map((p) => {
                return {
                    'id': p.id,
                    'filterDescription': p.name
                }
            })))

    const fetchProjects = async () => {
        storeError.resetMessages()
        const response = await axios.get('projects')
        projects.value = response.data.data
    }

    // This function is "private" - not exported by the store
    const getIndexOfProject = (projectId) => {
        return projects.value.findIndex((p) => p.id === projectId)
    }
    
    const fetchProject = async (projectId) => {
        storeError.resetMessages()
        const response = await axios.get('projects/' + projectId)
        const index = getIndexOfProject(projectId)
        if (index > -1) {
            // Instead of a direct assignment, object is cloned/copied to the array
            // This ensures that the object in the array is not the same as the object fetched
            projects.value[index] = Object.assign({}, response.data.data)  
        }
        return response.data.data
    }

    const insertProject = async (project) => {
        storeError.resetMessages()
        try {
            const response = await axios.post('projects', project)
            projects.value.push(response.data.data)
            toast({
                description: `Project #${response.data.data.id} 
                              "${response.data.data.name}" was created!`,
                action: h(ToastAction, {
                    altText: `Open new project`,
                    onclick: () => {
                        router.push({ name: 'updateProject', 
                                      params: {id: response.data.data.id} })
                    }
                }, {
                    default: () => `Open new project`,
                })
            })
            return response.data.data
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error creating project!')
            return false
        }
    }

    const updateProject = async (project) => {
        storeError.resetMessages()
        try {
            const response = await axios.put('projects/' + project.id, project)
            const index = getIndexOfProject(project.id)
            if (index > -1) {
                // Instead of a direct assignment, object is cloned/copied to the array
                // This ensures that the object in the array is not the same as the object fetched
                projects.value[index] = Object.assign({}, response.data.data)  
            }
            toast({
                description: 'Project has been updated correctly!',
            })
            return response.data.data
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error updating project!')
            return false
        }
    }

    const deleteProject = async (project) => {
        storeError.resetMessages()
        try {
            await axios.delete('projects/' + project.id)
            const index = getIndexOfProject(project.id)
            if (index > -1) {
                projects.value.splice(index, 1)
            }
            return true
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error deleting project!')
            return false
        }
    }    

    return {
        projects, totalProjects, listProjectsIncludingNull, listProjectsToFilter,
        fetchProjects, fetchProject, insertProject, updateProject, deleteProject
    }
})

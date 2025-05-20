import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useErrorStore } from '@/stores/error'
import { useRouter } from 'vue-router'
import { useToast } from '@/components/ui/toast/use-toast'
import { ToastAction } from '@/components/ui/toast'
import { h } from 'vue'

export const useTaskStore = defineStore('task', () => {
    const router = useRouter()
    const { toast } = useToast()
    const storeError = useErrorStore()

    const tasks = ref([])
    const filterByProject = ref(null)
    const filterByCompleted = ref(null)
    
    const totalTasks = computed(() => {
        return tasks.value ? tasks.value.length : 0
    })

    const totalFilteredTasks = computed(() => {
        return filteredTasks.value ? filteredTasks.value.length : 0
    })
    
    // This function is "private" - not exported by the store
    const taskInFilter = (task) => {
        if (filterByCompleted.value) {
            if (filterByCompleted.value.completed !== task.completed) {
                return false
            }
        }
        if (filterByProject.value) {
            if (filterByProject.value.id === -1) {
                if (task.project) {
                    return false
                }
            } else {
                if (!task.project) {
                    return false
                }
                if (filterByProject.value.id !== task.project.id) {
                    return false
                }
            }
        }
        return true
    }

    const filteredTasks = computed(() => tasks.value.filter(taskInFilter))

    const filterDescription = computed(() => {
        if (!filterByCompleted.value && !filterByProject.value) {
            return 'All tasks'
        }
        let description = ''
        if (filterByCompleted.value) {
            description += filterByCompleted.value.filterDescription
        } else {
            description += 'Tasks'
        }
        if (filterByProject.value) {
            if (filterByProject.value.id === -1) {
                description += ' with no project'
            } else {
                description += ' from project ' + filterByProject.value.filterDescription
            }
        }
        return description
    })

    const fetchTasks = async () => {
        storeError.resetMessages()
        const response = await axios.get('tasks')
        tasks.value = response.data.data
    }

    // This function is "private" - not exported by the store
    const getIndexOfTask = (taskId) => {
        return tasks.value.findIndex((p) => p.id === taskId)
    }
    
    const fetchTask = async (taskId) => {
        storeError.resetMessages()
        const response = await axios.get('tasks/' + taskId)
        const index = getIndexOfTask(taskId)
        if (index > -1) {
            // Instead of a direct assignment, object is cloned/copied to the array
            // This ensures that the object in the array is not the same as the object fetched
            tasks.value[index] = Object.assign({}, response.data.data)  
        }
        return response.data.data
    }

    const insertTask = async (task) => {
        storeError.resetMessages()
        try {
            const response = await axios.post('tasks', task)
            tasks.value.push(response.data.data)
            toast({
                description: `Task #${response.data.data.id} was created!`,
                action: h(ToastAction, {
                    altText: `Open new task`,
                    onclick: () => {
                        router.push({ name: 'updateTask', 
                                      params: {id: response.data.data.id} })
                    }
                }, {
                    default: () => `Open new task`,
                })
            })
            return response.data.data
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error inserting task!')
            return false
        }
    }

    const updateTask = async (task) => {
        storeError.resetMessages()
        try {
            task.project_id = task.project ? task.project.id : null
            const response = await axios.put('tasks/' + task.id, task)
            const index = getIndexOfTask(task.id)
            if (index > -1) {
                // Instead of a direct assignment, object is cloned/copied to the array
                // This ensures that the object in the array is not the same as the object fetched
                tasks.value[index] = Object.assign({}, response.data.data)  
            }
            toast({
                description: 'Task has been updated correctly!',
            })
            return response.data.data
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error updating task!')
            return false
        }
    }

    const toggleCompletedTask = async (task) => {
        let requestBody = {
            completed: !task.completed
        }
        storeError.resetMessages()
        try {
            const response = await axios.patch('tasks/' + task.id + '/completed', requestBody)
            const index = getIndexOfTask(task.id)
            if (index > -1) {
                // Instead of a direct assignment, object is cloned/copied to the array
                // This ensures that the object in the array is not the same as the object fetched
                tasks.value[index] = Object.assign({}, response.data.data)  
            }
            return response.data.data
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error updating task!')
            return false
        }
    }   

    const deleteTask = async (task) => {
        storeError.resetMessages()
        try {
            await axios.delete('tasks/' + task.id)
            const index = getIndexOfTask(task.id)
            if (index > -1) {
                tasks.value.splice(index, 1)
            }
            return true
        } catch (e) {
            storeError.setErrorMessages(e.response.data.message, e.response.data.errors, e.response.status, 'Error deleting task!')
            return false
        }
    }     

    return {
        tasks, totalTasks, totalFilteredTasks, filteredTasks,
        filterDescription, filterByProject, filterByCompleted, 
        fetchTasks, fetchTask, insertTask, updateTask, deleteTask, toggleCompletedTask
    }
})

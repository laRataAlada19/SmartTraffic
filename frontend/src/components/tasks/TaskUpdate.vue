<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import TaskForm from './TaskForm.vue'
import { useTaskStore } from '@/stores/task'
import { useErrorStore } from '@/stores/error'

const storeTask = useTaskStore()
const storeError = useErrorStore()

const router = useRouter()

const task = ref(null)

const props = defineProps({
    id: {
        type: Number,
        required: true
    }
})

// When the "id" prop changes, the "task" will be loaded from the API
watch(
    () => props.id,
    async (newIDValue) => {
        task.value = await storeTask.fetchTask(newIDValue)
    },
    { immediate: true }
)

const save = async (task) => {
    if (await storeTask.updateTask(task)) {        
        router.push({name: 'tasks'})
    }
}

const cancel = () => {
    storeError.resetMessages()
    router.back()
}
</script>

<template>
    <TaskForm v-if="task" :task="task" :title="`Update Task #${ task.id }`" @save="save" @cancel="cancel"></TaskForm>
</template>
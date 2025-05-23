<script setup>
import { onMounted } from 'vue'
import TaskList from './TaskList.vue'
import NewTask from './NewTask.vue'
import FilterTasksForm from './TasksFilterForm.vue'
//import { useTaskStore } from '@/stores/task'
import { useErrorStore } from '@/stores/error'
import { useAuthStore } from '@/stores/auth'; 

const storeAuth = useAuthStore() 
const storeTask = useTaskStore()
const storeError = useErrorStore()

onMounted(() => {
    storeError.resetMessages()
})
</script>

<template>
    <div class="pt-4">
        <NewTask v-if="storeAuth.user"></NewTask> 
        <FilterTasksForm 
            v-model:filterByProject="storeTask.filterByProject" 
            v-model:filterByStatus="storeTask.filterByCompleted">
        </FilterTasksForm>
        <h2 class="pt-8 pb-2 text-2xl">
            {{ storeTask.filterDescription }}
            <span class="text-base">(Total = {{ storeTask.totalFilteredTasks }})</span> 
        </h2>
        <div v-show="storeTask.totalFilteredTasks > 0">
            <TaskList :tasks="storeTask.filteredTasks" :readonly="!storeAuth.user"></TaskList> 
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';
import LocationsList from './LocationList.vue';
import LocationCreate from './LocationCreate.vue';
import { useAuthStore } from '@/stores/auth';

const locationName = ref('');
const direction = ref('');
const locationStore = useLocationStore();
const storeAuth = useAuthStore();

onMounted(async () => {
    locationStore.fetchLocations();
});
</script>

<template>
    <!--
    <div v-if="!storeAuth.user" class="dashboard-wrapper">
        <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
        <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
    </div>
    <div v-else>
        -->
    <h1 class="dashboard-title">Localizações</h1>

    <div v-if="locationStore.totalLocations > 0" class="flex flex-col items-center">
        <LocationsList :locations="locationStore.locations" />
    </div>
    <div v-else class="flex flex-col items-center">
        <h1 class="text-2xl font-bold mb-4">Nenhuma localização encontrada</h1>
    </div>
    
    <br />
    <br />

    <LocationCreate />
    <!--</div>-->
</template>

<style scoped>
.dashboard-title {
    font-size: 1.75rem;
    font-weight: bold;
    color: #5BC0BE;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #5BC0BE;
    padding-bottom: 0.5rem;
}
</style>
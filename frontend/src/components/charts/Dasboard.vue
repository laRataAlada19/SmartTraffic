<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import Location from '../locations/Location.vue';
import LocationList from '../locations/LocationList.vue';


const locationName = ref('');
const direction = ref('');
const locationStore = useLocationStore();


onMounted(async () => {
    locationStore.fetchLocations();
});
</script>

<template>
    <div class="dashboard-container">
        <div v-if="locationStore.totalLocations > 0" class="flex flex-col items-center">
            <LocationList :locations="locationStore.locations" />
        </div>
        <div v-else class="flex flex-col items-center">
            <h1 class="text-2xl font-bold mb-4">Nenhuma localização encontrada</h1>
        </div>

        <ChartDisplay :selectedCharts="selectedCharts" />
    </div>
</template>
<style scoped>
.dashboard-container {
    margin-top: 80px;
    /* Ajuste o valor conforme necessário */
    padding: 20px;
    /* Opcional: Adiciona espaçamento interno */
}
</style>

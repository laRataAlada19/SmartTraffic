<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import Location from '../locations/Location.vue';
import LocationList from '../locations/LocationList.vue';
import { useAuthStore } from '@/stores/auth';

const locationName = ref('');
const direction = ref('');
const locationStore = useLocationStore();
const storeAuth = useAuthStore();

const selectedCharts = ref([]);

onMounted(async () => {
    try {
        locationStore.fetchLocations();
        console.log('Locations fetched:', locationStore.locations);

        const tables = await storeAuth.getTables();
        console.log('Tables fetched:', tables);

        if (tables && tables.tables && tables.tables.Dashboard) {
            selectedCharts.value = tables.tables.Dashboard;
        }
    } catch (error) {
        console.error('Erro ao buscar tabelas ou gráficos:', error.message);
        router.push({ name: 'login' });
    }
});
</script>

<template>
    <div v-if="!storeAuth.user" class="dashboard-wrapper">
        <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
        <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
    </div>
    <div v-else>
        <br>
        <br>
        <br>
        <br>
        <div class="dashboard-container">
            <div v-if="locationStore.totalLocations > 0" class="flex flex-col items-center">
                <LocationList :locations="locationStore.locations" />
            </div>
            <div v-else class="flex flex-col items-center">
                <p>Sem localizações disponíveis.</p>
            </div>

            <div v-if="selectedCharts.length > 0" class="charts-wrapper">
                <h2>Gráficos Selecionados</h2>
                <ChartDisplay :selectedCharts="selectedCharts" />
            </div>
            <div v-else>
                <p>Nenhum gráfico selecionado.</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.dashboard-container {
    margin-top: 20px;
    padding: 20px;
}

.charts-wrapper {
    margin-top: 20px;
}
</style>
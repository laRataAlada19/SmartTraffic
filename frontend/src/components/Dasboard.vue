<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import LocationList from '@/components/locations/LocationList.vue';
import { useAuthStore } from '@/stores/auth';
import { useFactVehicleStore } from '@/stores/factvehicle';
import { toast } from './ui/toast';

const locationStore = useLocationStore();
const factVehicleStore = useFactVehicleStore();
const storeAuth = useAuthStore();
const totalVehicles = ref(0);
const totalCars = ref(0);
const totalBikes = ref(0);
const totalTrucks = ref(0);
const totalBuses = ref(0);
const totalMotorcycles = ref(0);
const mostMovimentedStrests = ref([]);
const lessMovimentedStrests = ref([]);
const selectedCharts = ref([]);
const theme = ref(1);
const selectedDate = ref(new Date().toISOString().split('T')[0]); // Data atual no formato YYYY-MM-DD
const refreshTime = ref('')

const changeTheme = (selectedTheme) => {
    theme.value = selectedTheme;
    fetchSummary();
};

const fetchSummary = async () => {
    try {
        const payload = {
            date: selectedDate.value,
            theme: theme.value,
        };
        totalVehicles.value = await factVehicleStore.fetchTotalVehicles(payload);
        totalCars.value = await factVehicleStore.fetchTotalCars(payload);
        totalBikes.value = await factVehicleStore.fetchTotalBikes(payload);
        totalTrucks.value = await factVehicleStore.fetchTotalTrucks(payload);
        totalBuses.value = await factVehicleStore.fetchTotalBuses(payload);
        totalMotorcycles.value = await factVehicleStore.fetchTotalMotorcycles(payload);
        mostMovimentedStrests.value = await factVehicleStore.fetchMostMovimentedStress(payload);
        lessMovimentedStrests.value = await factVehicleStore.fetchLessMovimentedStress(payload);
    } catch (error) {
        console.error('Erro ao buscar dados estatisticos:', error);
        toast({
            title: 'Erro',
            description: 'Não foi possível buscar os dados estatisticos. Tente novamente mais tarde.',
            type: 'error',
        });
    }
};

onMounted(async () => {
    try {
        locationStore.fetchLocations();
        await fetchSummary();
        const tables = await storeAuth.getTables();
        const now = new Date()
        refreshTime.value = now.toLocaleString()

        if (tables && tables.tables && tables.tables.Dashboard) {
            selectedCharts.value = tables.tables.Dashboard;
        }
    } catch (error) {
        console.error('Erro ao buscar tabelas ou gráficos:', error.message);
        toast({
            title: 'Erro',
            description: 'Ocorreu um erro ao buscar as tabelas ou gráficos. Por favor, tente novamente.',
            type: 'error',
        });
        //router.push({ name: 'login' });
    }
});
</script>

<template>
    <!--
    <div v-if="!storeAuth.user" class="dashboard-wrapper">
        <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
        <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
    </div>
    <div v-else>-->
    <h1 class="dashboard-title">Dashboard</h1>
    <div class="dashboard-container">
        <!-- LOCATIONS & STATS SECTION -->
        <div class="top-section">
            <!-- SUMMARY SECTION -->
            <div class="summary-column">
                <div class="theme-buttons">
                    <button @click="changeTheme(1)" :class="{ 'active': theme === 1 }">Diário</button>
                    <button @click="changeTheme(2)" :class="{ 'active': theme === 2 }">Semanal</button>
                    <button @click="changeTheme(3)" :class="{ 'active': theme === 3 }">Mensal</button>
                    <button @click="changeTheme(4)" :class="{ 'active': theme === 4 }">Anual</button>
                </div>
                <div class="date-picker">
                    <label for="date">Data base:</label>
                    <input id="date" type="date" v-model="selectedDate" />
                </div>
                <div class="stats-grid">
                    <div class="stat-card">Total de veículos: {{ totalVehicles }}</div>
                    <div class="stat-card">Total de ligeiros: {{ totalCars }}</div>
                    <div class="stat-card">Total de motas: {{ totalMotorcycles }}</div>
                    <div class="stat-card">Total de camiões: {{ totalTrucks }}</div>
                    <div class="stat-card">Total de autocarros: {{ totalBuses }}</div>
                    <div class="stat-card">Total de bicicletas: {{ totalBikes }}</div>
                    <div class="stat-card">Mais movimentada: {{ mostMovimentedStrests[0]?.location_name || 'N/A' }}
                    </div>
                    <div class="stat-card">Menos movimentada: {{ lessMovimentedStrests[0]?.location_name || 'N/A' }}
                    </div>
                    <div class="stat-card">Veículos em excesso: 11</div>
                    <div class="stat-card">Hora com mais tráfego: 18-19</div>
                    <div class="stat-card">Hora com menos tráfego: 02-03</div>
                    <div class="stat-card">Comparação com há 7 dias: +2%</div>
                </div>
            </div>
            <!-- LOCATIONS SECTION -->
            <div class="locations-column">
                <p>Localizações existentes</p>
                <div v-if="locationStore.totalLocations > 0">
                    <LocationList :locations="locationStore.locations" />
                </div>
                <div v-else>
                    <p>Sem localizações disponíveis.</p>
                </div>
            </div>
        </div>
        <!-- CHARTS SECTION -->
        <div v-if="selectedCharts.length > 0" class="charts-wrapper">
            <h2>Gráficos Selecionados</h2>
            <ChartDisplay :selectedCharts="selectedCharts" />
        </div>
        <div v-else>
            <p>Nenhum gráfico selecionado.</p>
        </div>
        <!-- LAST UPDATED -->
        <p class="updated-date">Atualizado em: {{ refreshTime }}</p>
    </div>
    <!-- </div>-->
</template>

<style scoped>
.dashboard-container {
    padding: 80px 24px 40px;
    background-color: #0B132B;
    color: white;
    min-height: 100vh;
}

.dashboard-title {
    font-size: 1.75rem;
    font-weight: bold;
    color: #5BC0BE;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #5BC0BE;
    padding-bottom: 0.5rem;
}

.theme-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.theme-buttons button {
    background-color: #1C2541;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background 0.3s;
}

.theme-buttons button:hover {
    background-color: #3A506B;
}

.theme-buttons .active {
    background-color: #5BC0BE;
    color: #0B132B;
    font-weight: bold;
}

.charts-wrapper {
    background-color: #1C2541;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
}

.top-section {
    display: flex;
    gap: 30px;
    flex-wrap: wrap;
    margin-bottom: 40px;
}

.locations-column {
    flex: 1;
    min-width: 300px;
    background-color: #1C2541;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
}

.locations-column p {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 10px;
    color: #5BC0BE;
}

.summary-column {
    flex: 2;
    min-width: 400px;
}

.date-picker {
    margin-bottom: 20px;
    color: #B0BEC5;
}

.date-picker input {
    padding: 8px;
    background-color: #1C2541;
    color: #FFFFFF;
    border: 1px solid #5BC0BE;
    border-radius: 5px;
    font-size: 1rem;
    margin-left: 10px;
}

.updated-date {
    font-size: 0.875rem;
    color: #5BC0BE;
    margin-top: 10px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.stat-card {
    background-color: #1C2541;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
    color: #FFFFFF;
    font-size: 1rem;
    font-weight: 500;
    text-align: left;
    transition: transform 0.2s;
}

.stat-card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 15px rgba(91, 192, 190, 0.3);
}
</style>
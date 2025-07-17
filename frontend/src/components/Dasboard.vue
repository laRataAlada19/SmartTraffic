<script setup>
import { ref, onMounted, watch } from 'vue';
import { useLocationStore } from '@/stores/location';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import LocationList from '@/components/locations/LocationList.vue';
import { useAuthStore } from '@/stores/auth';
import { useFactVehicleStore } from '@/stores/factvehicle';
import { toast } from '@/components/ui/toast';

/*Definir Stores*/
const locationStore = useLocationStore();
const factVehicleStore = useFactVehicleStore();
const storeAuth = useAuthStore();
/*Definir variaveis reactivas*/
const totalVehicles = ref(0);
const totalCars = ref(0);
const totalBikes = ref(0);
const totalTrucks = ref(0);
const totalBuses = ref(0);
const totalMotorcycles = ref(0);
const excesso= ref(0);
const mostMovimentedStrests = ref([]);
const lessMovimentedStrests = ref([]);
const selectedCharts = ref([]);
const theme = ref(1);
const selectedDate = ref(new Date().toISOString().split('T')[0]);
const refreshTime = ref('')
const data = ref([]);
const avg= ref(0);
const hourWithMostTraffic = ref('0');
const hourWithLessTraffic = ref('0');
/*Esta funçao serve para ir buscar a informação consoante a presente no filtro*/ 
const changeTheme = (selectedTheme) => {
    theme.value = selectedTheme;
    fetchSummary();
};
/*Esta funçao serve para ir buscar a informação*/
const fetchSummary = async () => {
    try {
        /*Verifica se o utilizador está autenticado antes de ir buscar os dados*/
        if (!storeAuth.user) {
            toast({
                title: 'Acesso Negado',
                description: 'Por favor, faça login para acessar o dashboard.',
                variant: 'destructive',
            });
            return;
        }
        /*Carregar os dados filtrados com base na data selecionada e no tema*/
        const payload = {
            date: selectedDate.value,
            theme: theme.value,
        };
        /*Vai buscar os dados filtrados*/
        data.value = await factVehicleStore.fetchDataFiltered(payload);
        totalCars.value = data.value.reduce((acc, item) => acc + item.car, 0);
        totalBikes.value = data.value.reduce((acc, item) => acc + item.bike, 0);
        totalTrucks.value = data.value.reduce((acc, item) => acc + item.truck, 0);
        totalBuses.value = data.value.reduce((acc, item) => acc + item.bus, 0);
        totalMotorcycles.value = data.value.reduce((acc, item) => acc + item.motorcycle, 0);
        totalVehicles.value = totalCars.value + totalBikes.value + totalTrucks.value + totalBuses.value + totalMotorcycles.value;
        excesso.value = data.value.reduce((acc, item) => acc + item.excess_speed, 0);
        avg.value = (data.value.reduce((acc, item) => acc + Number(item.average_speed), 0) )/ totalVehicles.value;
        mostMovimentedStrests.value = await factVehicleStore.fetchMostMovimentedStress(payload);
        lessMovimentedStrests.value = await factVehicleStore.fetchLessMovimentedStress(payload);
        for (const item of data.value) {
            if (item.hour_with_most_traffic) {
                hourWithMostTraffic.value = item.hour_with_most_traffic;
            }
            if (item.hour_with_less_traffic) {
                hourWithLessTraffic.value = item.hour_with_less_traffic;
            }
        }
        
    } catch (error) {
        toast({
            title: 'Erro',
            description: 'Não foi possível buscar os dados estatisticos. Tente novamente mais tarde.',
            variant: 'destructive',
        });
    }
};
/*Esta funçao serve para atualizar os dados quando a data selecionada for alterada*/
watch(selectedDate, (newDate) => {
    fetchSummary();
});

onMounted(async () => {
    try {
        locationStore.fetchLocations();
        await fetchSummary();
        const tables = await storeAuth.getTables();
        const now = new Date()
        refreshTime.value = now.toLocaleString()

        if (tables && tables.tables && tables.tables.Dashboard) {
            selectedCharts.value = tables.tables.Dashboard;
            console.log('Gráficos selecionados:', selectedCharts.value);
        }
    } catch (error) {
        console.error('Erro ao buscar tabelas ou gráficos:', error.message);
        toast({
            title: 'Erro',
            description: 'Ocorreu um erro ao buscar as tabelas ou gráficos. Por favor, tente novamente.',
            type: 'error',
        });
    }
});
</script>

<template>
    <div v-if="!storeAuth.user" class="dashboard-wrapper">
        <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
        <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
    </div>
    <div v-else>
    <h1 class="dashboard-title">Dashboard</h1>
    <div class="dashboard-container">
        <div class="top-section">
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
                    <div class="stat-card">Veículos em excesso: {{ excesso }} </div>
                    <div class="stat-card">Velocidade média: {{ avg }} km/h</div>
                </div>
            </div>
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
        <div v-if="selectedCharts.length > 0" class="charts-wrapper">
            <h2>Gráficos Selecionados</h2>
            <ChartDisplay :selectedCharts="selectedCharts" />
        </div>
        <div v-else>
            <p>Nenhum gráfico selecionado.</p>
        </div>
        <p class="updated-date">Atualizado em: {{ refreshTime }}</p>
    </div>
    </div>
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
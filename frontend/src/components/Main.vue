<script setup>
import { ref, onMounted, watch } from 'vue';
import { useLocationStore } from '@/stores/location';
import { useRoute } from 'vue-router';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import { useFactVehicleStore } from '@/stores/factvehicle';
import { useAuthStore } from '@/stores/auth';

const locationStore = useLocationStore();
const factVehicleStore = useFactVehicleStore();
const storeAuth = useAuthStore();
const route = useRoute();

const theme = ref(1); 
const selectedDate = ref(new Date().toISOString().split('T')[0]);

const selectedCharts = ref(route.query.charts ? route.query.charts.split(',') : []);

const totalVehicles = ref(0);
const totalCars = ref(0);
const totalBikes = ref(0);
const totalTrucks = ref(0);
const totalBuses = ref(0);
const totalMotorcycles = ref(0);
const mostMovimentedStrests = ref([]);
const lessMovimentedStrests = ref([]);

const changeTheme = (selectedTheme) => {
  theme.value = selectedTheme;
  fetchSummary();
};

const fetchSummary = async () => {
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
};

watch(selectedDate, fetchSummary);

onMounted(async () => {
  locationStore.fetchLocations();
  await fetchSummary();
});
</script>

<template>
  <div class="dashboard-wrapper">
    <div style="padding: 70px 10px 0;">
      <h1>O meu dashboard:</h1>
      <div class="dashboard-container">
        <h1>Resumo:</h1>
        <div class="theme-buttons">
          <button @click="changeTheme(1)" :class="{ 'active': theme === 1 }">Diário</button>
          <button @click="changeTheme(2)" :class="{ 'active': theme === 2 }">Semanal</button>
          <button @click="changeTheme(3)" :class="{ 'active': theme === 3 }">Mensal</button>
          <button @click="changeTheme(4)" :class="{ 'active': theme === 4 }">Anual</button>
        </div>

        <div style="margin-bottom: 20px;">
          <label for="date">Data base:</label>
          <input id="date" type="date" v-model="selectedDate"
            style="padding: 8px; border: 1px solid #ccc; border-radius: 5px; font-size: 1rem;" />
        </div>

        <div class="gray-box">
          <div class="stats-left">
            <h3>Total de veículos: {{ totalVehicles }}</h3>
            <h3>Total de ligeiros: {{ totalCars }}</h3>
            <h3>Total de motas: {{ totalMotorcycles }}</h3>
            <h3>Total de camiões: {{ totalTrucks }}</h3>
            <h3>Total de autocarros: {{ totalBuses }}</h3>
            <h3>Total de bicicletas: {{ totalBikes }}</h3>
          </div>
          <div class="stats-right">
            <h3>Mais movimentada: {{ mostMovimentedStrests[0]?.location_name || 'N/A' }}</h3>
            <h3>Menos movimentada: {{ lessMovimentedStrests[0]?.location_name || 'N/A' }}</h3>
            <h3>Veículos em excesso: 11</h3>
            <h3>Hora com mais tráfego: 18-19</h3>
            <h3>Hora com menos tráfego: 02-03</h3>
            <h3>Comparação com há 7 dias: +2%</h3>
          </div>
        </div>
        </div>

      <ChartDisplay :selectedCharts="selectedCharts" />
    </div>
  </div>
</template>


<style scoped>
.dashboard-wrapper {
  padding: 20px;
}
.dashboard-wrapper h1 {
  color: #0A1425;
}
.dashboard-container {
  background-color: #D9D9D9;
  padding: 20px;
  border-radius: 10px;
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.location-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.location-buttons button {
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 5px;
}

.theme-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.theme-buttons button {
  padding: 8px 16px;
  background-color: #FFFFFF;
  color: #000000;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.theme-buttons button:hover {
  background-color: #f0f0f0;
}

.theme-buttons button.active {
  background-color: #0A1425;
  color: #FFFFFF;
  border-color: #0A1425;
}

.daily-summary {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.date-picker {
  display: flex;
  align-items: center;
  gap: 10px;
}

.date-picker input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.gray-box {
  background-color: #FFFFFF;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 20px;
}
.gray-box h3 {
  color: #0A1425;
}

.stats-left,
.stats-right {
  flex: 1 1 300px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-width: 250px;
}

.stats-right {
  border-left: 1px solid #eee;
  padding-left: 20px;
}

/* Responsivo para ecrãs pequenos */
@media (max-width: 768px) {
  .gray-box {
    flex-direction: column;
  }

  .stats-right {
    border-left: none;
    padding-left: 0;
  }
}
</style>
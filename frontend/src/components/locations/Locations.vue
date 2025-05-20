<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';
import LocationsGraficos from './LocationsGraficos.vue'; 
import { useFactVehicleStore } from '@/stores/factvehicle';


const locationName = ref(''); // Campo para o nome da nova localização
const direction = ref(''); // Campo para a direção da câmera
const locationStore = useLocationStore(); // Acessar o store de localização
const theme = ref(1); // Tema inicial
const factVehicleStore = useFactVehicleStore();

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
};
const getTotalVehicles = async () => {
    totalVehicles.value = await factVehicleStore.fetchTotalVehicles();
    totalCars.value = await factVehicleStore.fetchTotalCars();
    totalBikes.value = await factVehicleStore.fetchTotalBikes();
    totalTrucks.value = await factVehicleStore.fetchTotalTrucks();
    totalBuses.value = await factVehicleStore.fetchTotalBuses();
    totalMotorcycles.value = await factVehicleStore.fetchTotalMotorcycles();
    mostMovimentedStrests.value = await factVehicleStore.fetchMostMovimentedStress();
    lessMovimentedStrests.value = await factVehicleStore.fetchLessMovimentedStress();
};

onMounted(async () => {
  locationStore.fetchLocations();
  await getTotalVehicles();

});
</script>
<template>
  <div style="display: flex; justify-content: center; padding: 70px 10px 0;">
    <h1 style="margin-bottom: 20px;">O meu dashboard:</h1>
    <div
      style="
        background-color: #D9D9D9;
        padding: 25px;
        border-radius: 10px;
        margin-top: 10px;
        width: 100%;
        max-width: 90%;
        margin-left: auto;
        margin-right: auto;
      "
    >
      <h1>Resumo:</h1>
      <div class="theme-buttons">
        <button @click="changeTheme(1)" :class="{ 'active': theme === 1 }">
          Diário
        </button>
        <button @click="changeTheme(2)" :class="{ 'active': theme === 2 }">
          Semanal
        </button>
        <button @click="changeTheme(3)" :class="{ 'active': theme === 3 }">
          Mensal
        </button>
        <button @click="changeTheme(4)" :class="{ 'active': theme === 4 }">
          Anual
        </button>
      </div>
      <div v-if="theme === 1">
        <h2>Diário</h2>
        <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 15px;">
          <div style="display: flex; align-items: center; gap: 15px;">
            <h2 style="margin: 0; font-size: 1.2rem;">Data:</h2>
            <input id="date" type="date" v-model="selectedDate"
              style="padding: 8px; border: 1px solid #ccc; border-radius: 5px; font-size: 1rem;" />
          </div>

          <div style="background-color: #FFFFFF; padding: 25px; border-radius: 10px; display: flex; width: 100%; gap: 30px;">

            <div style="flex: 1;">
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Total de veículos: {{ totalVehicles }}  </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Total de veículos ligeiros: {{ totalCars }} </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Total de motas: {{ totalMotorcycles }} </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Total de camiões: {{ totalTrucks }} </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Total de autocarros: {{ totalBuses }} </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Total de bicicletas: {{ totalBikes }} </h3>
            </div>

            <div style="flex: 1; padding-left: 30px; border-left: 1px solid #eee;">
              <h3 style="margin: 12px 0; font-size: 1.1rem;">
                Localização mais movimentada: {{ mostMovimentedStrests[0]?.location_name || 'N/A' }}
              </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Localização menos movimentada: {{ lessMovimentedStrests[0]?.location_name || 'N/A' }} </h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Veículos em excesso de velocidade: 11</h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Hora com mais tráfego: 18-19</h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Hora com menos tráfego: 02-03</h3>
              <h3 style="margin: 12px 0; font-size: 1.1rem;">Comparação resultados de a 7 dias: +2%</h3>
            </div>
          </div>
        </div>
        <p style="margin-top: 20px; font-size: 1rem;">Resumo diário de dados.</p>
      </div>

      <div v-if="theme === 2"><h2>Semanal</h2><p>Resumo semanal de dados.</p></div>
      <div v-if="theme === 3"><h2>Mensal</h2><p>Resumo mensal de dados.</p></div>
      <div v-if="theme === 4"><h2>Anual</h2><p>Resumo anual de dados.</p></div>
    </div>

    <LocationsGraficos v-if="theme === 1" :selectedDate="selectedDate" :location="selectedLocation" />

  </div>
</template>

<style scoped>
.dashboard-wrapper {
  padding: 20px;
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

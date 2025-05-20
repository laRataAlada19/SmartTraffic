<script setup>
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
import LocationList from '@/components/locations/LocationList.vue';
import LocationCreate from '@/components/locations/LocationCreate.vue';

const locationName = ref('');
const direction = ref('');
const locationStore = useLocationStore();
const granularity = ref(1); //default diário

const changeGranularity = (selectedGranularity) => {
    granularity.value = selectedGranularity;
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

    await locationStore.fetchLocations();
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
    <br>
    <br>
    <br>
    <br>

    <div v-if="locationStore.totalLocations > 0">
        <LocationList :locations="locationStore.locations"></LocationList>
    </div>
    <div v-else>
        <p class="text-center">Nenhum local encontrado.</p>
    </div>

    <br>
    <br>
    <br>
    <br>

    <LocationCreate></LocationCreate>
</template>
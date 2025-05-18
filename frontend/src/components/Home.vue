<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';
import { embedDashboard } from '@superset-ui/embedded-sdk';

const locationName = ref(''); // Campo para o nome da nova localização
const direction = ref(''); // Campo para a direção da câmera
const locationStore = useLocationStore(); // Acessar o store de localização

const createLocation = async () => {
  try {
    // Verifica se os campos estão preenchidos
    if (!locationName.value || !direction.value) {
      alert('Por favor, preencha todos os campos.');
      return;
    }
    // Atualiza o store com a nova localização
    locationStore.addLocation(locationName.value, direction.value);
    // Limpa os campos após a criação
    locationName.value = '';
    direction.value = '';
  } catch (error) {
    console.error('Erro ao criar localização:', error);
  }
};

onMounted(async () => {
  locationStore.fetchLocations();
  await embedDashboard({
    id: "12", // ID do dashboard no Superset
    supersetDomain: "http://localhost:8088", // onde o Superset está a correr
    mountPoint: document.getElementById("superset-container"), // div onde vai ser injetado
    fetchGuestToken: () =>
      fetch("http://localhost:8000/api/superset-token").then(res => res.text()),
    dashboardUiConfig: {
      hideTitle: true,
      hideChartControls: true,
      hideTabBar: true,
    }
  });
});
</script>

<template>
  <div>
    <h1>O meu dashboard:</h1>
    <ul>
      <li v-for="location in locationStore.locations" :key="location.id">
        {{ location.location_id }}:{{ location.location }} - {{ location.direction }}
      </li>
      <li v-if="locationStore.locations.length === 0">
        No locations available.
      </li>
    </ul>
    <div>
      <input v-model="locationName" type="text" placeholder="Digite o nome da localização" />
      <input v-model="direction" type="text" placeholder="Digite a direção da camera" />
      <button @click="createLocation">Criar Localização</button>
    </div>
  </div>
  <div id="superset-container" style="width: 100%; height: 800px;"></div>
  <iframe src="http://localhost:8088/superset/dashboard/12" width="100%" height="800" frameborder="0"></iframe>
</template>
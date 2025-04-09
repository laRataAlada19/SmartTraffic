<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';

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

onMounted(() => {
  locationStore.fetchLocations();
});

</script>

<template>
  <div>
    <h1>Location List</h1>
    <ul>
      <li v-for="location in locationStore.locations" :key="location.id">
       {{ location.location_id }}:{{ location.location }} - {{ location.direction }}
      </li>
      <li v-if="locationStore.locations.length === 0">
        No locations available.
      </li>
    </ul>
    <iframe
  width="600"
  height="400"
  seamless
  frameBorder="0"
  scrolling="no"
  src="http://localhost:8088/superset/explore/p/0br91Yq1aYM/?standalone=1&height=400"
>
</iframe>

    <!-- Formulário para criar nova localização -->
    <div>
      <input v-model="locationName" type="text" placeholder="Digite o nome da localização"/>
      <input v-model="direction" type="text" placeholder="Digite a direção da camera"/>
      <button @click="createLocation">Criar Localização</button>
    </div>
  </div>
</template>
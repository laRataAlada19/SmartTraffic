<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';

const locationName = ref(''); // Campo para o nome da nova localização
const direction = ref(''); // Campo para a direção da câmera
const locationStore = useLocationStore(); // Acessar o store de localização

// Função para criar uma nova localização
const createLocation = async () => {
  if (locationName.value.trim() === '') {
    alert('O nome da localização não pode estar vazio.');
    return;
  }

  try {
    await addLocation(locationName.value, direction.value); // Chama a função do store
    locationName.value = ''; // Limpa o campo de entrada
    direction.value = ''; // Limpa o campo de direção
    alert('Localização criada com sucesso!');
  } catch (error) {
    console.error('Erro ao criar localização:', error);
    alert('Erro ao criar localização.');
  }
};

const addLocation = async (name, direction) => {
  try {
    const response = await axios.post('/api/locations', {
      name,
      direction,
    });
    locationStore.locations.push(response.data);
  } catch (error) {
    console.error('Erro ao adicionar localização:', error);
    throw error;
  }
};
</script>

<template>
  <div>
    <h1>Location List</h1>
    <ul>
      <li v-for="location in locationStore.locations" :key="location.id">
        {{ location.name }}
      </li>
      <li v-if="locationStore.locations.length === 0">
        No locations available.
      </li>
    </ul>

    <!-- Formulário para criar nova localização -->
    <div>
      <input v-model="locationName" type="text" placeholder="Digite o nome da localização"/>
      <input v-model="direction" type="text" placeholder="Digite a direção da camera"/>
      <button @click="createLocation">Criar Localização</button>
    </div>
  </div>
</template>
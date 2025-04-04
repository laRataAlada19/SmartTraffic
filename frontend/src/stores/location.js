import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';


export const useLocationStore = defineStore('location', () => {
  const locations = ref([]);

  // Função para buscar localizações
  const fetchLocations = async () => {
    try {
      const response = await axios.get('/api/locations');
      console.log("aqui" , response.data);
      locations.value = response.data;
    } catch (error) {
      console.error('Erro ao buscar locais:', error);
    }
  };

  // Função para adicionar uma nova localização
  const addLocation = async (location,direction) => {
    try {
     console.log("loc",location);
    console.log("dir",direction);
      const response = await axios.post('/api/locations', { location ,direction});
      locations.value.push(response.data); // Atualiza o estado local com a nova localização

    } catch (error) {
      console.error('Erro ao adicionar localização:', error);
      throw error;
    }
  };

  return {
    locations,
    fetchLocations,
    addLocation,
  };
});
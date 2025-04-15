import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';


export const useLocationStore = defineStore('location', () => {
  const locations = ref([]);

  // Função para buscar localizações
  const fetchLocations = async () => {
    try {
      const response = await axios.get('/api/locations');
      console.log("aqui" , response.data.data);
      locations.value = response.data.data;
    } catch (error) {
      console.error('Erro ao buscar locais:', error);
    }
  };

  // Função para adicionar uma nova localização
  const addLocation = async (location, direction) => {
    try {
      const response = await axios.post('/api/locations', null, {
        params: {
          location: location,
          direction: direction,
        },
      });
      locations.value.push(response.data); // Atualiza o estado local com a nova localização
    } catch (error) {
      console.error('Erro ao adicionar localização:', error);
      throw error;
    }
  };

  const deleteLocation = async (locationId) => {
    try {
      await axios.delete(`/api/locations/${locationId}`);
      locations.value = locations.value.filter(location => location.id !== locationId);
    } catch (error) {
      console.error('Erro ao excluir localização:', error);
      throw error;
    }
  }

  const updateLocation = async (locationId, updatedLocation) => {
    try {
      const response = await axios.put(`/api/locations/${locationId}`, updatedLocation);
      const index = locations.value.findIndex(location => location.id === locationId);
      if (index !== -1) {
        locations.value[index] = response.data;
      }
    } catch (error) {
      console.error('Erro ao atualizar localização:', error);
      throw error;
    }
  }


  return {
    locations,
    fetchLocations,
    addLocation,
    deleteLocation,
    updateLocation
  };
});
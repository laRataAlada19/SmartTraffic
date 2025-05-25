import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useLocationStore = defineStore('location', () => {
  const locations = ref([]);

  const totalLocations = computed(() => {
    return locations.value ? locations.value.length : 0
  })

  const fetchLocations = async () => {
    try {
      const response = await axios.get('/locations');
      locations.value = response.data.data;
    } catch (error) {
      console.error('Erro ao buscar locais:', error);
    }
  };

  const fetchLocationById = async (locationId) => {
    try {
      const response = await axios.get(`/locations/${locationId}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar localização:', error);
      throw error;
    }
  };

  const addLocation = async (location, direction, latitude, longitude) => {
    try {
      const response = await axios.post('/locations', null, {
        params: {
          location: location,
          direction: direction,
          latitude: latitude,
          longitude: longitude,
        },
      });
      locations.value.push(response.data); 
    } catch (error) {
      console.error('Erro ao adicionar localização:', error);
      throw error;
    }
  };

  const deleteLocation = async (locationId) => {
    try {
      await axios.delete(`/locations/${locationId}`);
      locations.value = locations.value.filter(location => location.id !== locationId);
    } catch (error) {
      console.error('Erro ao excluir localização:', error);
      throw error;
    }
  }

  const updateLocation = async (locationId, updatedLocation) => {
    try {
      const response = await axios.patch(`/locations/${locationId}`, updatedLocation);
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
    updateLocation,
    fetchLocationById,
    totalLocations,
  };
});
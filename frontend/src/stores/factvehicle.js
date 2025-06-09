import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useFactVehicleStore = defineStore('factvehicle', () => {
    const factvehicles = ref([]);
    const factvehicle = ref(null);

    const fetchData = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts');
            factvehicles.value = response.data.data;
            return factvehicles.value;
        } catch (error) {
            console.error('Erro ao buscar dados:', error);
        }
    };

    const fetchTotalVehicles = async ({ date, theme }) => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total', {
                params: { date, theme }
            });
            return response.data.total_vehicle_count;
        } catch (error) {
            console.error('Erro ao buscar veículos:', error);
            return null;
        }
    };

    const fetchTotalByType = async (type, { date, theme }) => {
        try {
            const response = await axios.get(`/fact-vehicle-counts/total/${type}`, {
                params: { date, theme }
            });
            return response.data[`total_${type}_count`];
        } catch (error) {
            console.error(`Erro ao buscar ${type}:`, error);
            return null;
        }
    };

    const fetchTotalCars = (payload) => fetchTotalByType('car', payload);
    const fetchTotalMotorcycles = (payload) => fetchTotalByType('motorcycle', payload);
    const fetchTotalTrucks = (payload) => fetchTotalByType('truck', payload);
    const fetchTotalBikes = (payload) => fetchTotalByType('bike', payload);
    const fetchTotalBuses = (payload) => fetchTotalByType('bus', payload);

    const fetchMostMovimentedStress = async ({ date, theme }) => {
        try {
            const response = await axios.get('/fact-vehicle-counts/must-movimented-streets', {
                params: { date, theme }
            });
            return response.data.most_movimented_stress;
        } catch (error) {
            console.error('Erro ao buscar mais movimentados:', error);
            return null;
        }
    };

    const fetchLessMovimentedStress = async ({ date, theme }) => {
        try {
            const response = await axios.get('/fact-vehicle-counts/less-movimented-streets', {
                params: { date, theme }
            });
            return response.data.less_movimented_stress;
        } catch (error) {
            console.error('Erro ao buscar menos movimentados:', error);
            return null;
        }
    };

    return {
        factvehicles,
        factvehicle,
        fetchData,
        fetchTotalVehicles,
        fetchTotalCars,
        fetchTotalMotorcycles,
        fetchTotalTrucks,
        fetchTotalBikes,
        fetchTotalBuses,
        fetchMostMovimentedStress,
        fetchLessMovimentedStress,
    };
});

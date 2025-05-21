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
            console.log('Dados recebidos:', factvehicles.value);
            return factvehicles.value;
        } catch (error) {
            console.error('Erro ao buscar dados:', error);
        }
    }
    const fetchTotalVehicles = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total');
            const totalVehicles = response.data.total_vehicle_count;
            return totalVehicles;
        } catch (error) {
            console.error('Erro ao buscar veículos:', error);
            return null;
        }
    };
    const fetchTotalCars = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total/car');
            const totalCars = response.data.total_car_count;
            return totalCars;
        } catch (error) {
            console.error('Erro ao buscar carros:', error);
            return null;
        }
    };
    const fetchTotalMotorcycles = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total/motorcycle');
            const totalMotorcycles = response.data.total_motorcycle_count;
            return totalMotorcycles;
        } catch (error) {
            console.error('Erro ao buscar motocicletas:', error);
            return null;
        }
    }

    const fetchTotalTrucks = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total/truck');
            const totalTrucks = response.data.total_truck_count;
            return totalTrucks;
        } catch (error) {
            console.error('Erro ao buscar caminhões:', error);
            return null;
        }
    };
    const fetchTotalBikes = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total/bike');
            const totalBikes = response.data.total_bike_count;
            return totalBikes;
        } catch (error) {
            console.error('Erro ao buscar motos:', error);
            return null;
        }
    };
    const fetchTotalBuses = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total/bus');
            const totalBuses = response.data.total_bus_count;
            return totalBuses;
        } catch (error) {
            console.error('Erro ao buscar ônibus:', error);
            return null;
        }
    };
    const fetchMostMovimentedStress = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/must-movimented-streets');
            const mostMovimentedStress = response.data.most_movimented_stress;
            return mostMovimentedStress;
        } catch (error) {
            console.error('Erro ao buscar mais movimentados:', error);
            return null;
        }
    }
    const fetchLessMovimentedStress = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/less-movimented-streets');
            const lessMovimentedStress = response.data.less_movimented_stress;
            return lessMovimentedStress;
        } catch (error) {
            console.error('Erro ao buscar menos movimentados:', error);
            return null;
        }
    }

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
}
);
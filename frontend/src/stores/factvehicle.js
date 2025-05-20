import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';


export const useFactVehicleStore = defineStore('factvehicle', () => {
    const factvehicles = ref([]);
    const factvehicle = ref(null);

    const fetchTotalVehicles = async () => {
        try {
            const response = await axios.get('/fact-vehicle-counts/total');
            const totalVehicles = response.data.total_vehicle_count;
            console.log('Total de veículos:', totalVehicles);
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
            console.log('Total de carros:', totalCars);
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
            console.log('Total de motocicletas:', totalMotorcycles);
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
            console.log('Total de caminhões:', totalTrucks);
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
            console.log('Total de motos:', totalBikes);
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
            console.log('Total de ônibus:', totalBuses);
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
            console.log('Mais movimentados:', mostMovimentedStress);
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
            console.log('Menos movimentados:', lessMovimentedStress);
            return lessMovimentedStress;
        } catch (error) {
            console.error('Erro ao buscar menos movimentados:', error);
            return null;
        }
    }


    
    return {
        factvehicles,
        factvehicle,
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
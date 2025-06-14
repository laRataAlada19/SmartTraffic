<script setup>
import { ref, computed, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js';
import { useFactVehicleStore } from '@/stores/factvehicle';
import dayjs from 'dayjs';
import { useSharedData } from '@/components/charts/useSharedData';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement);

const store = useFactVehicleStore();
const locationFilter = ref('Todos');
const timeInterval = ref('dia');
const data1 = ref([]);

const { sharedData } = useSharedData();


const getVehicleDataByType = (type) => {
  const locationsSet = [...new Set(data1.value.map(d => d.location || 'Desconhecido'))];
  return locationsSet.map(loc => {
    const locEntries = data1.value.filter(d => d.location === loc);
    return locEntries.reduce((sum, entry) => sum + (entry[type] || 0), 0);
  });
};

const chartData = computed(() => ({
  labels: [...new Set(data1.value.map(d => d.location || 'Desconhecido'))],
  datasets: [
    {
      label: 'Veículos',
      data: getVehicleDataByType('car'),
      backgroundColor: 'rgba(75, 192, 192, 0.5)',
      borderColor: 'rgb(75, 192, 192)',
      borderWidth: 1
    }
  ]
}));

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    title: {
      display: true,
      text: 'Gráfico de Barras'
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Categorias'
      }
    },
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Valores'
      }
    }
  }
};

onMounted(async () => {
  data1.value= sharedData.value;
  console.log("BarChart data fetched:", data1.value);
});
</script>

<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/PieChart.vue
import { ref, computed } from 'vue';
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  Filler, 
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

// Accept the preloaded data as a prop
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');

const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

const aggregatedVehicleCounts = computed(() => {
  if (!Array.isArray(props.data)) return {};

  let filteredData = [...props.data];

  if (locationFilter.value !== 'Todos') {
    filteredData = filteredData.filter(d => d.location === locationFilter.value);
  }

  const totals = {
    car: 0,
    motorcycle: 0,
    bike: 0,
    truck: 0,
    bus: 0,
  };

  filteredData.forEach(entry => {
    totals.car += entry.car;
    totals.motorcycle += entry.motorcycle;
    totals.bike += entry.bike;
    totals.truck += entry.truck;
    totals.bus += entry.bus;
  });

  return totals;
});

const chartData = computed(() => ({
  labels: ['Carro', 'Moto', 'Bicicleta', 'Caminhão', 'Ônibus'],
  datasets: [
    {
      label: 'Contagem de Veículos',
      data: [
        aggregatedVehicleCounts.value.car,
        aggregatedVehicleCounts.value.motorcycle,
        aggregatedVehicleCounts.value.bike,
        aggregatedVehicleCounts.value.truck,
        aggregatedVehicleCounts.value.bus,
      ],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 1,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
    title: {
      display: true,
      text: 'Gráfico de Pizza - Contagem de Veículos',
    },
  },
};
</script>

<template>
  <div>
    <div style="margin-bottom: 1rem;">
      <label>Localidade:
        <select v-model="locationFilter">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>
    </div>

    <Pie :data="chartData" :options="chartOptions" />
  </div>
</template>
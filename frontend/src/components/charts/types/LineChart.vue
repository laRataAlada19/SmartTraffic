<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/LineChart.vue
import { ref, computed } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,   
} from 'chart.js';
import dayjs from 'dayjs';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

// Accept the preloaded data as a prop
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');
const timeInterval = ref('dia');

const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

const filteredData = computed(() => {
  if (!Array.isArray(props.data)) return [];

  let filtered = [...props.data];

  if (locationFilter.value !== 'Todos') {
    filtered = filtered.filter(d => d.location === locationFilter.value);
  }

  const grouped = {};

  filtered.forEach(entry => {
    let key = '';

    switch (timeInterval.value) {
      case 'mes':
        key = `${entry.year}-${String(entry.month).padStart(2, '0')}`;
        break;
      case 'semana':
        key = dayjs(entry.full_date).startOf('week').format('YYYY-MM-DD');
        break;
      case 'dia':
      default:
        key = entry.full_date;
    }

    if (!grouped[key]) grouped[key] = 0;
    grouped[key] += entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus;
  });

  return Object.entries(grouped).sort((a, b) => new Date(a[0]) - new Date(b[0]));
});

const chartData = computed(() => ({
  labels: filteredData.value.map(d => d[0]),
  datasets: [
    {
      label: 'Total de Veículos',
      data: filteredData.value.map(d => d[1]),
      borderColor: 'rgb(75, 192, 192)',
      fill: false,
      tension: 0.1,
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
      text: 'Gráfico de Linha',
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

      <label style="margin-left: 2rem;">Intervalo:
        <select v-model="timeInterval">
          <option value="dia">Dia</option>
          <option value="semana">Semana</option>
          <option value="mes">Mês</option>
        </select>
      </label>
    </div>

    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>
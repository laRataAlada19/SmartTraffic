<script setup>
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
    <div class="filter-container">
      <label class="filter-label">
        Localidade:
        <select v-model="locationFilter" class="filter-select">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>

      <label class="filter-label">
        Intervalo:
        <select v-model="timeInterval" class="filter-select">
          <option value="dia">Dia</option>
          <option value="semana">Semana</option>
          <option value="mes">Mês</option>
        </select>
      </label>
    </div>

    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.filter-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-label {
  font-weight: 500;
  color: #fff;
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
}

.filter-select {
  margin-top: 0.3rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #fff;
  color: #333;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6; 
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
</style>

<script setup>
import { ref, computed } from 'vue';
import { Radar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';
import dayjs from 'dayjs';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  Title
);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');
const timeInterval = ref('dia');
const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];

const directionLabels = {
  n: 'Norte',
  ne: 'Nordeste',
  e: 'Leste',
  se: 'Sudeste',
  s: 'Sul',
  sw: 'Sudoeste',
  w: 'Oeste',
  nw: 'Noroeste',
};

const locations = computed(() => {
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

const filteredData = computed(() => {
  let data = [...props.data];

  if (locationFilter.value !== 'Todos') {
    data = data.filter(d => d.location === locationFilter.value);
  }

  const grouped = {};

  data.forEach(entry => {
    let key = '';
    switch (timeInterval.value) {
      case 'mes':
        key = `${entry.year}-${String(entry.month).padStart(2, '0')}`;
        break;
      case 'semana':
        key = dayjs(entry.full_date).startOf('week').format('YYYY-MM-DD');
        break;
      default:
        key = entry.full_date;
    }

    if (!grouped[key]) {
      grouped[key] = Object.fromEntries(directions.map(dir => [dir, 0]));
    }

    directions.forEach(dir => {
      grouped[key][dir] += entry[dir] || 0;
    });
  });

  return Object.values(grouped);
});

const totalByDir = computed(() =>
  directions.map(dir =>
    filteredData.value.reduce((sum, d) => sum + (d[dir] || 0), 0)
  )
);

const chartData = computed(() => ({
  labels: directions.map(dir => directionLabels[dir]),
  datasets: [
    {
      label: 'Tráfego por Direção',
      data: totalByDir.value,
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      pointBackgroundColor: 'rgba(54, 162, 235, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 2,
      fill: true,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
      },
    },
    title: {
      display: true,
      text: 'Radar de Direções de Tráfego',
      font: {
        size: 16,
      },
    },
    tooltip: {
      callbacks: {
        label: context => `${context.label}: ${context.parsed.r}`,
      },
    },
  },
  scales: {
    r: {
      beginAtZero: true,
      ticks: {
        stepSize: 1,
        backdropColor: 'transparent',
      },
      pointLabels: {
        font: {
          size: 14,
          weight: 'bold',
        },
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      },
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

    <div class="chart-container">
      <Radar :data="chartData" :options="chartOptions" />
    </div>
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

.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>

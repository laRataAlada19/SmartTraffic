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

// Props
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

// Filtros
const locationFilter = ref('Todos');
const timeInterval = ref('dia');

// Localidades únicas
const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

// Direções
const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];

// Filtragem de dados
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
      case 'dia':
      default:
        key = entry.full_date;
    }

    if (!grouped[key]) {
      grouped[key] = { ...Object.fromEntries(directions.map(dir => [dir, 0])) };
    }

    directions.forEach(dir => {
      grouped[key][dir] += entry[dir] || 0;
    });
  });

  return Object.values(grouped);
});

// Soma total por direção (com base nos dados filtrados)
const totalByDir = computed(() =>
  directions.map(dir =>
    filteredData.value.reduce((sum, d) => sum + (d[dir] || 0), 0)
  )
);

// Dados para o radar
const chartData = computed(() => ({
  labels: ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
  datasets: [
    {
      label: 'Direção de tráfego',
      data: totalByDir.value,
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      pointBackgroundColor: 'rgba(75, 192, 192, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(75, 192, 192, 1)',
    },
  ],
}));

// Opções do radar
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      beginAtZero: true,
      angleLines: {
        color: 'rgba(0,0,0,0.1)',
      },
      grid: {
        color: 'rgba(0,0,0,0.05)',
      },
      pointLabels: {
        font: {
          size: 14,
          weight: 'bold',
        },
        color: '#333',
      },
      ticks: {
        backdropColor: 'transparent',
        color: '#666',
        stepSize: 1,
      },
    },
  },
  plugins: {
    legend: {
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
        color: '#333',
      },
    },
    tooltip: {
      callbacks: {
        label: context => `${context.label}: ${context.parsed.r}`,
      },
    },
    title: {
      display: true,
      text: 'Radar de Direções de Tráfego',
      font: {
        size: 16,
      },
      color: '#111',
    },
  },
};
</script>

<template>
  <div>
    <!-- Filtros -->
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

    <!-- Gráfico -->
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

<script setup>
import { ref, computed } from 'vue';
import { Bar } from 'vue-chartjs';
import dayjs from 'dayjs';
import isoWeek from 'dayjs/plugin/isoWeek';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
);

dayjs.extend(isoWeek);

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

const directionNames = {
  n: 'Norte',
  ne: 'Nordeste',
  e: 'Leste',
  se: 'Sudeste',
  s: 'Sul',
  sw: 'Sudoeste',
  w: 'Oeste',
  nw: 'Noroeste'
};

const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});


const directionData = computed(() => {
  if (!Array.isArray(props.data)) return [];

  let filteredData = [...props.data];

  if (locationFilter.value !== 'Todos') {
    filteredData = filteredData.filter(d => d.location === locationFilter.value);
  }

  const grouped = {};

  filteredData.forEach(entry => {
    let key = '';

    switch (timeInterval.value) {
      case 'mes':
        key = `${entry.year}-${String(entry.month).padStart(2, '0')}`;
        break;
      case 'semana':
        key = dayjs(entry.full_date).startOf('isoWeek').format('YYYY-MM-DD');
        break;
      case 'dia':
      default:
        key = entry.full_date;
    }

    if (!grouped[key]) {
      grouped[key] = {};
      directions.forEach(dir => {
        grouped[key][dir] = 0;
      });
    }

    directions.forEach(dir => {
      grouped[key][dir] += entry[dir] || 0;
    });
  });

  return Object.entries(grouped).sort((a, b) => new Date(a[0]) - new Date(b[0]));
});

function getDirectionColors(dir, border = false) {
  const colors = {
    n: 'rgba(255, 99, 132, 0.7)',
    ne: 'rgba(255, 159, 64, 0.7)',
    e: 'rgba(255, 205, 86, 0.7)',
    se: 'rgba(75, 192, 192, 0.7)',
    s: 'rgba(54, 162, 235, 0.7)',
    sw: 'rgba(153, 102, 255, 0.7)',
    w: 'rgba(201, 203, 207, 0.7)',
    nw: 'rgba(255, 99, 255, 0.7)',
  };

  const borderColors = {
    n: 'rgba(255, 99, 132, 1)',
    ne: 'rgba(255, 159, 64, 1)',
    e: 'rgba(255, 205, 86, 1)',
    se: 'rgba(75, 192, 192, 1)',
    s: 'rgba(54, 162, 235, 1)',
    sw: 'rgba(153, 102, 255, 1)',
    w: 'rgba(201, 203, 207, 1)',
    nw: 'rgba(255, 99, 255, 1)',
  };

  return border ? borderColors[dir] : colors[dir];
}

const chartData = computed(() => {
  const labels = directionData.value.map(d => {
    switch (timeInterval.value) {
      case 'mes':
        return dayjs(d[0]).format('MMM YYYY');
      case 'semana':
        return `Sem ${dayjs(d[0]).format('DD/MM')}`;
      default:
        return dayjs(d[0]).format('DD/MM/YYYY');
    }
  });

  const datasets = directions.map(dir => ({
    label: directionNames[dir], 
    data: directionData.value.map(d => d[1][dir]),
    backgroundColor: getDirectionColors(dir),
    borderColor: getDirectionColors(dir, true),
    borderWidth: 1,
    borderRadius: 4,
  }));

  return { labels, datasets };
});

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
      text: 'Fluxo de Tráfego por Direção',
      font: {
        size: 16,
      },
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          label += context.parsed.y;
          return label;
        }
      }
    },
  },
  scales: {
    x: {
      stacked: false,
      grid: {
        display: false,
      },
      title: {
        display: true,
        text: 'Período Temporal',
      },
    },
    y: {
      stacked: false,
      beginAtZero: true,
      title: {
        display: true,
        text: 'Número de Veículos',
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      },
    },
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false,
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
      <Bar :data="chartData" :options="chartOptions" />
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
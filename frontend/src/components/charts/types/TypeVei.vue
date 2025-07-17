<script setup>
import { ref, computed } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
} from 'chart.js';
import dayjs from 'dayjs';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, Filler);

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


const vehicleTypeData = computed(() => {
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
        key = dayjs(entry.full_date).startOf('week').format('YYYY-MM-DD');
        break;
      case 'dia':
      default:
        key = entry.full_date;
    }

    if (!grouped[key]) {
      grouped[key] = { 
        date: key,
        car: 0, 
        motorcycle: 0, 
        bike: 0, 
        truck: 0, 
        bus: 0 
      };
    }

    grouped[key].car += entry.car || 0;
    grouped[key].motorcycle += entry.motorcycle || 0;
    grouped[key].bike += entry.bike || 0;
    grouped[key].truck += entry.truck || 0;
    grouped[key].bus += entry.bus || 0;
  });

  return Object.values(grouped).sort((a, b) => new Date(a.date) - new Date(b.date));
});

const chartData = computed(() => ({
  labels: vehicleTypeData.value.map(d => {
    switch (timeInterval.value) {
      case 'mes':
        return dayjs(d.date).format('MMM YYYY');
      case 'semana':
        return `Sem ${dayjs(d.date).format('DD/MM')}`;
      default:
        return dayjs(d.date).format('DD/MM/YYYY');
    }
  }),
  datasets: [
    {
      label: 'Carros',
      data: vehicleTypeData.value.map(d => d.car),
      backgroundColor: 'rgba(54, 162, 235, 0.7)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
    {
      label: 'Motos',
      data: vehicleTypeData.value.map(d => d.motorcycle),
      backgroundColor: 'rgba(255, 99, 132, 0.7)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
    {
      label: 'Bicicletas',
      data: vehicleTypeData.value.map(d => d.bike),
      backgroundColor: 'rgba(255, 206, 86, 0.7)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
    {
      label: 'Camiões',
      data: vehicleTypeData.value.map(d => d.truck),
      backgroundColor: 'rgba(75, 192, 192, 0.7)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
    {
      label: 'Autocarros',
      data: vehicleTypeData.value.map(d => d.bus),
      backgroundColor: 'rgba(153, 102, 255, 0.7)',
      borderColor: 'rgba(153, 102, 255, 1)',
      borderWidth: 1,
      borderRadius: 4,
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
      text: 'Evolução de Tipos de Veículos',
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
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
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');
const hourFilter = ref('Todos');

const availableHours = computed(() => {
  if (!Array.isArray(props.data)) return [];
  return [...new Set(props.data.map(entry => entry.hour))]
    .sort((a, b) => a - b)
    .map(hour => ({
      value: hour,
      label: `${hour}:00 - ${hour+1}:00`
    }));
});

const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

const groupedData = computed(() => {
  if (!Array.isArray(props.data)) return [];

  let filteredData = [...props.data];

  if (locationFilter.value !== 'Todos') {
    filteredData = filteredData.filter(d => d.location === locationFilter.value);
  }

  if (hourFilter.value !== 'Todos') {
    filteredData = filteredData.filter(d => d.hour === parseInt(hourFilter.value));
  }

  const groupedByHour = {};

  filteredData.forEach(entry => {
    const hour = entry.hour;
    if (!groupedByHour[hour]) {
      groupedByHour[hour] = {
        total: 0,
        car: 0,
        motorcycle: 0,
        bike: 0,
        truck: 0,
        bus: 0,
      };
    }

    groupedByHour[hour].total += entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus;
    groupedByHour[hour].car += entry.car;
    groupedByHour[hour].motorcycle += entry.motorcycle;
    groupedByHour[hour].bike += entry.bike;
    groupedByHour[hour].truck += entry.truck;
    groupedByHour[hour].bus += entry.bus;
  });

  return Object.entries(groupedByHour)
    .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
    .map(([hour, values]) => ({
      hour: parseInt(hour),
      ...values
    }));
});

const chartData = computed(() => ({
  labels: groupedData.value.map(item => `${item.hour}:00`),
  datasets: [
    {
      label: 'Total de Veículos',
      data: groupedData.value.map(item => item.total),
      backgroundColor: 'rgba(54, 162, 235, 0.7)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1,
      borderRadius: 4,
    },
    {
      label: 'Carros',
      data: groupedData.value.map(item => item.car),
      backgroundColor: 'rgba(255, 99, 132, 0.7)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1,
      borderRadius: 4,
      hidden: true,
    },
    {
      label: 'Motociclos',
      data: groupedData.value.map(item => item.motorcycle),
      backgroundColor: 'rgba(255, 206, 86, 0.7)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 1,
      borderRadius: 4,
      hidden: true,
    },
    {
      label: 'Bicicletas',
      data: groupedData.value.map(item => item.bike),
      backgroundColor: 'rgba(75, 192, 192, 0.7)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
      borderRadius: 4,
      hidden: true,
    },
    {
      label: 'Camiões',
      data: groupedData.value.map(item => item.truck),
      backgroundColor: 'rgba(153, 102, 255, 0.7)',
      borderColor: 'rgba(153, 102, 255, 1)',
      borderWidth: 1,
      borderRadius: 4,
      hidden: true,
    },
    {
      label: 'Autocarros',
      data: groupedData.value.map(item => item.bus),
      backgroundColor: 'rgba(255, 159, 64, 0.7)',
      borderColor: 'rgba(255, 159, 64, 1)',
      borderWidth: 1,
      borderRadius: 4,
      hidden: true,
    }
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
      onClick: (e, legendItem, legend) => {
        const index = legendItem.datasetIndex;
        const ci = legend.chart;
        const meta = ci.getDatasetMeta(index);
        
        meta.hidden = meta.hidden === null ? !ci.data.datasets[index].hidden : null;
        ci.update();
      }
    },
    title: {
      display: true,
      text: 'Distribuição de Tráfego por Hora do Dia',
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
        },
        footer: (tooltipItems) => {
          if (tooltipItems.length > 1) {
            const total = tooltipItems.reduce((sum, tooltipItem) => sum + tooltipItem.parsed.y, 0);
            return `Total: ${total}`;
          }
        }
      }
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Hora do Dia',
      },
      grid: {
        display: false,
      },
    },
    y: {
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
        Hora:
        <select v-model="hourFilter" class="filter-select">
          <option value="Todos">Todas as horas</option>
          <option v-for="hour in availableHours" :key="hour.value" :value="hour.value">
            {{ hour.label }}
          </option>
        </select>
      </label>

      <label class="filter-label">
        Localidade:
        <select v-model="locationFilter" class="filter-select">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
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
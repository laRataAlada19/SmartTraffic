<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/TypeVei.vue
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

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');
const timeInterval = ref('dia');

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

    if (!grouped[key]) grouped[key] = { car: 0, motorcycle: 0, bike: 0, truck: 0, bus: 0 };

    grouped[key].car += entry.car;
    grouped[key].motorcycle += entry.motorcycle;
    grouped[key].bike += entry.bike;
    grouped[key].truck += entry.truck;
    grouped[key].bus += entry.bus;
  });

  return Object.entries(grouped).map(([key, values]) => ({
    date: key,
    ...values,
  }));
});

const chartData = computed(() => ({
  labels: vehicleTypeData.value.map(d => d.date),
  datasets: [
    {
      label: 'Carros',
      data: vehicleTypeData.value.map(d => d.car),
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1,
    },
    {
      label: 'Motos',
      data: vehicleTypeData.value.map(d => d.motorcycle),
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1,
    },
    {
      label: 'Bicicletas',
      data: vehicleTypeData.value.map(d => d.bike),
      backgroundColor: 'rgba(255, 206, 86, 0.2)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 1,
    },
    {
      label: 'Camiões',
      data: vehicleTypeData.value.map(d => d.truck),
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    },
    {
      label: 'Autocarro',
      data: vehicleTypeData.value.map(d => d.bus),
      backgroundColor: 'rgba(153, 102, 255, 0.2)',
      borderColor: 'rgba(153, 102, 255, 1)',
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
      text: 'Tipos de Veículos por Período',
    },
  },
};
</script>

<template>
  <div>
    <div style="margin-bottom: 1rem;">
      <label>Localidade:
        <select v-model="locationFilter">
          <option value="Todos">Todos</option>
          <option v-for="loc in [...new Set(props.data.map(entry => entry.location))]" :key="loc" :value="loc">
            {{ loc }}
          </option>
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

    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
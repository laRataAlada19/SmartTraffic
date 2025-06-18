<script setup>
import { ref, computed, onMounted } from 'vue';
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
onMounted(() => {
  if (!props.data || !Array.isArray(props.data)) {
    console.warn('Dados inválidos recebidos em Direction.vue');
  }
  console.log('Dados recebidos em Direction.vue:', props.data);
console.log('Dados agrupados para gráfico:', directionData.value);

});


const locationFilter = ref('Todos');
const timeInterval = ref('dia');

const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
const propsData = props.data.length ? props.data : fakeData;

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

function getColorForDirection(dir, border = false) {
  const colors = {
    n: 'rgba(255, 99, 132, 0.2)',
    ne: 'rgba(255, 159, 64, 0.2)',
    e: 'rgba(255, 205, 86, 0.2)',
    se: 'rgba(75, 192, 192, 0.2)',
    s: 'rgba(54, 162, 235, 0.2)',
    sw: 'rgba(153, 102, 255, 0.2)',
    w: 'rgba(201, 203, 207, 0.2)',
    nw: 'rgba(255, 99, 255, 0.2)',
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
  const labels = directionData.value.map(d => d[0]);

  const datasets = directions.map(dir => ({
    label: dir.toUpperCase(),
    data: directionData.value.map(d => d[1][dir]),
    backgroundColor: getColorForDirection(dir),
    borderColor: getColorForDirection(dir, true),
    borderWidth: 1,
  }));

  return { labels, datasets };
});

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
    title: {
      display: true,
      text: 'Direção de Veículos',
    },
  },
};
</script>

<template>
   <p>Direction.vue está a renderizar!</p>
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

    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

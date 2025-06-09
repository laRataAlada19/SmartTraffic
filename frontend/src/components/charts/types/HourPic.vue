<script setup>
import { ref, computed, onMounted } from 'vue';
import { Bar } from 'vue-chartjs'; // Importa o componente Bar
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { useFactVehicleStore } from '@/stores/factvehicle';
import dayjs from 'dayjs';

// Registra os componentes necessários do Chart.js
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const store = useFactVehicleStore();
const locationFilter = ref('Todos');
const timeInterval = ref('dia');
const data1 = ref([]);
const hourFilter = ref('Todos');
const availableHours = computed(() => {
  if (!Array.isArray(data1.value)) return ['Todos'];
  const hours = [...new Set(data1.value.map(entry => entry.hour))];
  return ['Todos', ...hours.sort((a, b) => a - b)];
});

const peakHourData = computed(() => {
  if (!Array.isArray(data1.value)) return [];

  let data = [...data1.value];

  if (locationFilter.value !== 'Todos') {
    data = data.filter(d => d.location === locationFilter.value);
  }

  if (hourFilter.value !== 'Todos') {
    data = data.filter(d => d.hour === parseInt(hourFilter.value));
  }

  const groupedByHour = {};

  data.forEach(entry => {
    const hour = entry.hour;
    if (!groupedByHour[hour]) {
      groupedByHour[hour] = {
        total: 0,
        car: 0,
        motorcycle: 0,
        bike: 0,
        truck: 0,
        bus: 0
      };
    }

    const total = entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus;
    groupedByHour[hour].total += total;
    groupedByHour[hour].car += entry.car;
    groupedByHour[hour].motorcycle += entry.motorcycle;
    groupedByHour[hour].bike += entry.bike;
    groupedByHour[hour].truck += entry.truck;
    groupedByHour[hour].bus += entry.bus;
  });

  return Object.entries(groupedByHour).sort((a, b) => parseInt(a[0]) - parseInt(b[0]));
});
onMounted(async () => {
  if (!Array.isArray(data1.value) || data1.value.length === 0) {
    data1.value = await store.fetchData();
    console.log('Dados carregados:', data1.value);
  }
});
</script>

<template>
  <div>
    <div style="margin-bottom: 1rem;">
      <label>Hora:
        <select v-model="hourFilter">
          <option v-for="hour in availableHours" :key="hour" :value="hour">
            {{ hour === 'Todos' ? 'Todas' : `${hour}:00` }}
          </option>
        </select>
      </label>
    </div>
    
    <div style="margin-top: 3rem;">
      <Bar
        v-if="peakHourData.length"
        :data="{
          labels: peakHourData.map(d => `${d[0]}:00`),
          datasets: [{
            label: 'Total de Veículos',
            data: peakHourData.map(d => d[1].total),
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        }"
        :options="{
          responsive: true,
          plugins: {
            legend: { display: true },
            title: { display: true, text: 'Tráfego por Hora do Dia' }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }"
      />
      <p v-else>Nenhum dado disponível para análise de horário de pico.</p>
    </div>
  </div>
</template>
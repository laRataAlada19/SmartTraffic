<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/HourPic.vue
import { ref, computed } from 'vue';
import { Bar } from 'vue-chartjs';

// Accept the preloaded data as a prop
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
  return [...new Set(props.data.map(entry => entry.hour))].sort((a, b) => a - b);
});

const groupedData = computed(() => {
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

const chartData = computed(() => ({
  labels: groupedData.value.map(([hour]) => `${hour}:00`),
  datasets: [
    {
      label: 'Total de Veículos',
      data: groupedData.value.map(([_, values]) => values.total),
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1,
    },
  ],
}));
</script>

<template>
  <div>
    <div style="margin-bottom: 1rem;">
      <label>Hora:
        <select v-model="hourFilter">
          <option value="Todos">Todos</option>
          <option v-for="hour in availableHours" :key="hour" :value="hour">
            {{ hour }}:00
          </option>
        </select>
      </label>

      <label style="margin-left: 2rem;">Localidade:
        <select v-model="locationFilter">
          <option value="Todos">Todos</option>
          <option v-for="loc in [...new Set(props.data.map(entry => entry.location))]" :key="loc" :value="loc">
            {{ loc }}
          </option>
        </select>
      </label>
    </div>

    <Bar :data="chartData" :options="{ responsive: true }" />
  </div>
</template>
<script setup>
// filepath: /components/charts/types/Trend.vue

import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale,
  Filler } from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale);

// Props sem required, para permitir uso do default
const props = defineProps({
  data: {
    type: Array,
    default: () => [],
  },
});

// Computa total por dia, só se props.data for válida
const days = computed(() => {
  if (!Array.isArray(props.data)) return [];

  const grouped = {};
  props.data.forEach(d => {
    grouped[d.full_date] ??= 0;
    grouped[d.full_date] += d.car + d.motorcycle + d.bike + d.truck + d.bus;
  });

  return Object.entries(grouped).sort((a, b) => new Date(a[0]) - new Date(b[0]));
});
</script>

<template>
  <Line :data="{
    labels: days.map(([d]) => d),
    datasets: [{
      label: 'Total de veículos por dia',
      data: days.map(([_, v]) => v),
      borderColor: 'purple',
      fill: false
    }]
  }" :options="{ responsive: true }" />
</template>

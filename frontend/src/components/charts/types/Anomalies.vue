<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/Anomalies.vue
import { ref, computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale,
  Filler,  } from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

console.log('Anomalies data received:', props.data);

const totals = computed(() => {
  if (!props.data || props.data.length === 0) return [];
  return props.data.map(d => d.car + d.motorcycle + d.bike + d.truck + d.bus);
});

const labels = computed(() => {
  if (!props.data || props.data.length === 0) return [];
  return props.data.map(d => `${d.hour}:${String(d.minute).padStart(2, '0')}`);
});

const avg = computed(() => {
  if (totals.value.length === 0) return 0;
  return totals.value.reduce((a, b) => a + b, 0) / totals.value.length;
});

const anomalyIndices = computed(() => {
  if (totals.value.length === 0) return [];
  return totals.value.map((val, i) => (val > avg.value * 1.5 ? val : null));
});
</script>

<template>
  <Line v-if="totals.length > 0" :data="{
    labels,
    datasets: [
      {
        label: 'Tráfego',
        data: totals,
        borderColor: 'blue',
        fill: false
      },
      {
        label: 'Anomalias',
        data: anomalyIndices,
        borderColor: 'red',
        pointBackgroundColor: 'red',
        showLine: false
      }
    ]
  }" :options="{ responsive: true }" />
  <p v-else style="text-align: center; color: red;">Nenhum dado disponível para exibir.</p>
</template>
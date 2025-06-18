<script setup>
import { computed,onMounted } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler, 
} from 'chart.js';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

console.log('TrafficDensity data received:', props.data);
console.log('First item structure:', props.data[0] || 'No data');

const hasRequiredFields = computed(() => {
  if (!props.data || props.data.length === 0) return false;
  const firstItem = props.data[0];
  return 'hour' in firstItem && 'minute' in firstItem && 'car' in firstItem;
});

const minutes = computed(() => {
  if (!hasRequiredFields.value) return [];
  return props.data.map(d => `${d.hour}:${String(d.minute).padStart(2, '0')}`);
});

const totals = computed(() => {
  if (!hasRequiredFields.value) return [];
  return props.data.map(d => (d.car || 0) + (d.motorcycle || 0) + (d.bike || 0) + (d.truck || 0) + (d.bus || 0));
});
onMounted(() => {
  console.log('Componente montado com dados:', props.data);
  console.log('Tipo dos dados:', typeof props.data);
  console.log('É array?', Array.isArray(props.data));
});
</script>

<template>
  <div v-if="!hasRequiredFields" class="data-warning">
    <p>Dados não têm a estrutura esperada.</p>
    <p>Estrutura necessária: { hour, minute, car, motorcycle, bike, truck, bus }</p>
    <p>Dados recebidos: {{ props.data[0] || 'Nenhum dado' }}</p>
  </div>
  <Line v-else-if="totals.length > 0" :data="{
    labels: minutes,
    datasets: [{
      label: 'Veículos por minuto',
      data: totals,
      borderColor: 'blue',
      fill: false
    }]
  }" :options="{ responsive: true }" />
</template>

<style scoped>
.data-warning {
  color: red;
  padding: 1rem;
  border: 1px solid red;
  margin: 1rem 0;
}
</style>
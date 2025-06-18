<script setup>
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Filler
);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const processedData = computed(() => {
  return props.data.map(d => ({
    label: `${d.period}`,
    value: d.value,
  }));
});

const chartData = computed(() => {
  if (!processedData.value.length) {
    return {
      labels: [],
      datasets: [
        {
          label: 'Comparação de Períodos',
          data: [],
          borderColor: 'rgba(75, 192, 192, 1)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          fill: true,
        },
      ],
    };
  }

  return {
    labels: processedData.value.map(d => d.label),
    datasets: [
      {
        label: 'Comparação de Períodos',
        data: processedData.value.map(d => d.value),
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
      },
    ],
  };
});

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: true, position: 'top' },
    title: { display: true, text: 'Comparação de Períodos' },
  },
};
</script>

<template>
  <Line
    v-if="chartData && chartData.labels && chartData.datasets"
    :chart-data="chartData"
    :chart-options="chartOptions"
  />
</template>

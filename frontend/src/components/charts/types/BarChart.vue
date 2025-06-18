<script setup>
// filepath: BarChart.vue
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Filler, 
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

// Agrupar totais por tipo de veículo
const chartData = computed(() => {
  const totals = {
    Carro: 0,
    Motociclo: 0,
    Bicicleta: 0,
    Camião: 0,
    Autocarro: 0,
  };

  props.data.forEach(d => {
    totals.Carro += d.car || 0;
    totals.Motociclo += d.motorcycle || 0;
    totals.Bicicleta += d.bike || 0;
    totals.Camião += d.truck || 0;
    totals.Autocarro += d.bus || 0;
  });

  return {
    labels: Object.keys(totals),
    datasets: [
      {
        label: 'Total por Tipo de Veículo',
        data: Object.values(totals),
        backgroundColor: [
          '#36A2EB', // Carro
          '#FF6384', // Motociclo
          '#FFCE56', // Bicicleta
          '#4BC0C0', // Camião
          '#9966FF'  // Autocarro
        ],
        borderColor: '#444',
        borderWidth: 1,
      },
    ],
  };
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
      text: 'Distribuição por Tipo de Veículo',
    },
  },
  scales: {
    x: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Tipo de Veículo',
      },
    },
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Total de Veículos',
      },
    },
  },
};
</script>

<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

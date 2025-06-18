<script setup>
import { ref, watch, onMounted } from 'vue';
import { Chart as ChartJS, Tooltip, Title, Legend, LinearScale, CategoryScale } from 'chart.js';
import 'chartjs-chart-matrix';
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix';

ChartJS.register(
  Tooltip,
  Title,
  Legend,
  LinearScale,
  CategoryScale,
  MatrixController,
  MatrixElement
);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const chartInstance = ref(null);
const canvasRef = ref(null);

const heatmapData = () => {
  const result = [];
  const types = ['car', 'motorcycle', 'truck', 'bus'];

  props.data.forEach(entry => {
    types.forEach(type => {
      result.push({
        x: entry.hour,
        y: type,
        v: entry[type] || 0
      });
    });
  });

  return result;
};

const backgroundColorFn = (ctx) => {
  const value = ctx.dataset.data[ctx.dataIndex].v;
  const alpha = Math.min(1, value / 50);
  return `rgba(255, 99, 132, ${alpha})`;
};

const buildChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }

  chartInstance.value = new ChartJS(canvasRef.value.getContext('2d'), {
    type: 'matrix',
    data: {
      datasets: [{
        label: 'Tráfego',
        data: heatmapData(),
        backgroundColor: backgroundColorFn,
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top',
        },
        title: {
          display: true,
          text: 'Heatmap de Tráfego',
        },
        tooltip: {
          callbacks: {
            label: (ctx) => `Valor: ${ctx.raw.v}`,
          },
        },
      },
      scales: {
        x: {
          type: 'linear',
          title: {
            display: true,
            text: 'Hora',
          },
        },
        y: {
          type: 'category',
          title: {
            display: true,
            text: 'Tipo de Veículo',
          },
        },
      },
    },
  });
};

onMounted(() => {
  buildChart();
});
</script>

<template>
  <div>
    <h3>Heatmap de Tráfego</h3>
    <canvas ref="canvasRef" />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
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
const locationFilter = ref('Todos');
const timeInterval = ref('dia');

// Computed para localizações disponíveis
const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

// Computed para dados filtrados
const filteredData = computed(() => {
  if (!Array.isArray(props.data)) return [];
  
  let filtered = [...props.data];
  
  if (locationFilter.value !== 'Todos') {
    filtered = filtered.filter(d => d.location === locationFilter.value);
  }
  
  return filtered;
});

// Tipos de veículos com tradução
const vehicleTypes = [
  { id: 'car', label: 'Carros' },
  { id: 'motorcycle', label: 'Motociclos' },
  { id: 'bike', label: 'Bicicletas' },
  { id: 'truck', label: 'Camiões' },
  { id: 'bus', label: 'Autocarros' }
];

// Preparar dados para o heatmap
const heatmapData = computed(() => {
  const result = [];
  const hourCounts = {};

  // Inicializar contagens por hora e tipo
  for (let hour = 0; hour < 24; hour++) {
    hourCounts[hour] = {};
    vehicleTypes.forEach(type => {
      hourCounts[hour][type.id] = 0;
    });
  }

  // Somar os valores por hora e tipo
  filteredData.value.forEach(entry => {
    const hour = parseInt(entry.hour);
    vehicleTypes.forEach(type => {
      hourCounts[hour][type.id] += entry[type.id] || 0;
    });
  });

  // Formatando para o heatmap
  vehicleTypes.forEach(type => {
    for (let hour = 0; hour < 24; hour++) {
      result.push({
        x: hour,
        y: type.label,
        v: hourCounts[hour][type.id]
      });
    }
  });

  return result;
});

// Função para cores do heatmap
const backgroundColorFn = (ctx) => {
  const value = ctx.dataset.data[ctx.dataIndex].v;
  const maxValue = Math.max(...heatmapData.value.map(item => item.v), 1);
  const normalized = Math.min(1, value / maxValue);
  
  // Escala de cores: azul (baixo) -> amarelo -> vermelho (alto)
  if (normalized < 0.5) {
    const intensity = normalized * 2;
    return `rgba(75, 192, 192, ${intensity})`; // Azul
  } else {
    const intensity = (normalized - 0.5) * 2;
    return `rgba(255, ${Math.round(205 * (1 - intensity))}, 86, ${intensity + 0.5})`; // Amarelo -> Vermelho
  }
};

// Construir/atualizar o gráfico
const buildChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }

  if (!canvasRef.value) return;

  const maxValue = Math.max(...heatmapData.value.map(item => item.v), 1);

  chartInstance.value = new ChartJS(canvasRef.value.getContext('2d'), {
    type: 'matrix',
    data: {
      datasets: [{
        label: 'Intensidade de Tráfego',
        data: heatmapData.value,
        backgroundColor: backgroundColorFn,
        borderWidth: 0,
        width: ({chart}) => (chart.chartArea || {}).width / 24 - 1,
        height: ({chart}) => (chart.chartArea || {}).height / vehicleTypes.length - 1
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            generateLabels: () => {
              return [{
                text: 'Intensidade de Tráfego',
                fillStyle: 'rgba(255, 99, 132, 0.7)',
                strokeStyle: '#fff',
                lineWidth: 1,
                hidden: false
              }];
            }
          }
        },
        title: {
          display: true,
          text: 'Heatmap de Tráfego por Hora e Tipo de Veículo' + 
                (locationFilter.value !== 'Todos' ? ` - ${locationFilter.value}` : ''),
          font: {
            size: 16,
            weight: 'bold'
          }
        },
        tooltip: {
          callbacks: {
            title: (context) => {
              const data = context[0].raw;
              return `${data.y} às ${data.x}:00`;
            },
            label: (context) => {
              const data = context.raw;
              return `Veículos: ${data.v}`;
            }
          }
        },
      },
      scales: {
        x: {
          type: 'linear',
          min: 0,
          max: 23,
          offset: true,
          title: {
            display: true,
            text: 'Hora do Dia',
            font: {
              weight: 'bold'
            }
          },
          ticks: {
            stepSize: 1,
            callback: (value) => `${value}:00`
          },
          grid: {
            display: false
          }
        },
        y: {
          type: 'category',
          title: {
            display: true,
            text: 'Tipo de Veículo',
            font: {
              weight: 'bold'
            }
          },
          offset: true,
          grid: {
            display: false
          }
        }
      }
    },
  });
};

// Observar mudanças nos dados e reconstruir o gráfico
watch([filteredData, locationFilter], () => {
  buildChart();
});

onMounted(() => {
  buildChart();
});
</script>

<template>
  <div>
    <div class="filter-container">
      <label class="filter-label">
        Localidade:
        <select v-model="locationFilter" class="filter-select" @change="buildChart">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>
    </div>

    <div class="chart-container">
      <canvas ref="canvasRef" />
    </div>
  </div>
</template>

<style scoped>
.filter-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-label {
  font-weight: 500;
  color: #fff;
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
  min-width: 200px;
}

.filter-select {
  margin-top: 0.3rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #fff;
  color: #333;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.chart-container {
  position: relative;
  height: 500px;
  width: 100%;
  margin-top: 1rem;
}
</style>
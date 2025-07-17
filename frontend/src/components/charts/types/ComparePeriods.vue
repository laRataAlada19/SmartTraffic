<script setup>
import { ref, computed } from 'vue';
import { Bar } from 'vue-chartjs';
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
  LinearScale
);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
});

const day1 = ref('');
const day2 = ref('');
const selectedPeriod = ref('Todos');
const compareMode = ref('periodo');

const availableDays = computed(() => {
  const days = [...new Set(props.data.map(item => item.day))];
  return days.sort((a, b) => a - b);
});

const availablePeriods = computed(() => {
  return ['Todos', ...new Set(props.data.map(item => item.period))];
});

const comparisonData = computed(() => {
  if (!day1.value || !day2.value) return [];

  const filterData = (day, period) => {
    return props.data.filter(item => {
      const matchesDay = item.day === day;
      const matchesPeriod = period === 'Todos' || item.period === period;
      return matchesDay && matchesPeriod;
    });
  };

  const day1Data = filterData(day1.value, compareMode.value === 'periodo' ? selectedPeriod.value : 'Todos');
  const day2Data = filterData(day2.value, compareMode.value === 'periodo' ? selectedPeriod.value : 'Todos');

  return [
    { day: day1.value, data: day1Data },
    { day: day2.value, data: day2Data }
  ];
});

const chartData = computed(() => {
  if (comparisonData.value.length === 0) return { labels: [], datasets: [] };

  const vehicleTypes = ['Carro', 'Motociclo', 'Bicicleta', 'Camião', 'Autocarro'];
  const colors = [
    'rgba(54, 162, 235, 0.7)',
    'rgba(255, 99, 132, 0.7)',
    'rgba(255, 206, 86, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(153, 102, 255, 0.7)'
  ];

  const labels = comparisonData.value.map(item => {
    if (compareMode.value === 'periodo' && selectedPeriod.value !== 'Todos') {
      return `Dia ${item.day} (${selectedPeriod.value})`;
    }
    return `Dia ${item.day}`;
  });

 
  const datasets = vehicleTypes.map((type, index) => {
    const typeKey = {
      'Carro': 'car',
      'Motociclo': 'motorcycle',
      'Bicicleta': 'bike',
      'Camião': 'truck',
      'Autocarro': 'bus'
    }[type];

    return {
      label: type,
      data: comparisonData.value.map(item => {
        return item.data.reduce((sum, entry) => sum + (entry[typeKey] || 0), 0);
      }),
      backgroundColor: colors[index],
      borderColor: '#444',
      borderWidth: 1,
      borderRadius: 4
    };
  });


  datasets.unshift({
    label: 'Total',
    data: comparisonData.value.map(item => {
      return item.data.reduce((sum, entry) => {
        return sum + (entry.car || 0) + (entry.motorcycle || 0) + 
               (entry.bike || 0) + (entry.truck || 0) + (entry.bus || 0);
      }, 0);
    }),
    backgroundColor: 'rgba(101, 116, 136, 0.7)',
    borderColor: 'rgba(101, 116, 136, 1)',
    borderWidth: 1,
    borderRadius: 4
  });

  return {
    labels: labels,
    datasets: datasets
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20,
      }
    },
    title: {
      display: true,
      text: computed(() => {
        if (!day1.value || !day2.value) return 'Comparação entre Dias';
        if (compareMode.value === 'periodo' && selectedPeriod.value !== 'Todos') {
          return `Comparação no Período: ${selectedPeriod.value}`;
        }
        return 'Comparação Diária';
      }),
      font: {
        size: 16,
      },
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          label += context.parsed.y;
          return label;
        },
        footer: (tooltipItems) => {
          if (tooltipItems.length > 1) {
            const total = tooltipItems.reduce((sum, tooltipItem) => sum + tooltipItem.parsed.y, 0);
            return `Total: ${total}`;
          }
        }
      }
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: 'Dias Comparados',
      },
      grid: {
        display: false,
      },
    },
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Número de Veículos',
      },
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
      },
    },
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false,
  },
};
</script>

<template>
  <div>
    <div class="filter-container">
      <label class="filter-label">
        Dia 1:
        <select v-model="day1" class="filter-select">
          <option value="">Selecione</option>
          <option 
            v-for="day in availableDays" 
            :key="day" 
            :value="day"
            :disabled="day === day2"
          >
            Dia {{ day }}
          </option>
        </select>
      </label>

      <label class="filter-label">
        Dia 2:
        <select v-model="day2" class="filter-select">
          <option value="">Selecione</option>
          <option 
            v-for="day in availableDays" 
            :key="day" 
            :value="day"
            :disabled="day === day1"
          >
            Dia {{ day }}
          </option>
        </select>
      </label>

      <label class="filter-label">
        Modo:
        <select v-model="compareMode" class="filter-select">
          <option value="dia">Dia Inteiro</option>
          <option value="periodo">Por Período</option>
        </select>
      </label>

      <label v-if="compareMode === 'periodo'" class="filter-label">
        Período:
        <select v-model="selectedPeriod" class="filter-select">
          <option v-for="period in availablePeriods" :key="period" :value="period">
            {{ period }}
          </option>
        </select>
      </label>
    </div>

    <div class="chart-container">
      <Bar :data="chartData" :options="chartOptions" />
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
  min-width: 150px;
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
  height: 400px;
  width: 100%;
  margin-top: 1rem;
}
</style>
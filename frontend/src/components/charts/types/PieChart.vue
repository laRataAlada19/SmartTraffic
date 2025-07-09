<script setup>
import { ref, computed } from 'vue';
import { Pie } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import dayjs from 'dayjs';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');
const timeInterval = ref('dia');
const dateRange = ref({
  start: '',
  end: ''
});

// Computed para localizações disponíveis
const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

// Computed para dados filtrados e agregados
const aggregatedVehicleCounts = computed(() => {
  if (!Array.isArray(props.data)) return {};

  let filteredData = [...props.data];

  // Filtro por localização
  if (locationFilter.value !== 'Todos') {
    filteredData = filteredData.filter(d => d.location === locationFilter.value);
  }

  // Filtro por intervalo de tempo
  if (timeInterval.value === 'custom' && dateRange.value.start && dateRange.value.end) {
    filteredData = filteredData.filter(d => {
      const date = dayjs(d.full_date);
      return date.isAfter(dayjs(dateRange.value.start).subtract(1, 'day')) && 
             date.isBefore(dayjs(dateRange.value.end).add(1, 'day'));
    });
  } else if (timeInterval.value !== 'custom') {
    const now = dayjs();
    filteredData = filteredData.filter(d => {
      const date = dayjs(d.full_date);
      switch (timeInterval.value) {
        case 'semana': return date.isAfter(now.subtract(1, 'week'));
        case 'mes': return date.isAfter(now.subtract(1, 'month'));
        case 'ano': return date.isAfter(now.subtract(1, 'year'));
        default: return true; // 'dia' ou outros
      }
    });
  }

  // Calcular totais
  const totals = {
    car: 0,
    motorcycle: 0,
    bike: 0,
    truck: 0,
    bus: 0,
  };

  filteredData.forEach(entry => {
    totals.car += entry.car || 0;
    totals.motorcycle += entry.motorcycle || 0;
    totals.bike += entry.bike || 0;
    totals.truck += entry.truck || 0;
    totals.bus += entry.bus || 0;
  });

  return totals;
});

// Configuração dos dados do gráfico
const chartData = computed(() => {
  const counts = aggregatedVehicleCounts.value;
  const total = counts.car + counts.motorcycle + counts.bike + counts.truck + counts.bus;

  return {
    labels: [
      `Carros (${total ? ((counts.car / total) * 100).toFixed(1) : 0}%)`,
      `Motociclos (${total ? ((counts.motorcycle / total) * 100).toFixed(1) : 0}%)`,
      `Bicicletas (${total ? ((counts.bike / total) * 100).toFixed(1) : 0}%)`,
      `Camiões (${total ? ((counts.truck / total) * 100).toFixed(1) : 0}%)`,
      `Autocarros (${total ? ((counts.bus / total) * 100).toFixed(1) : 0}%)`
    ],
    datasets: [{
      data: [
        counts.car,
        counts.motorcycle,
        counts.bike,
        counts.truck,
        counts.bus,
      ],
      backgroundColor: [
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
      ],
      borderColor: [
        'rgba(54, 162, 235, 1)',
        'rgba(255, 99, 132, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
      ],
      borderWidth: 1,
      hoverOffset: 10
    }]
  };
});

// Opções do gráfico
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right',
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 12
        }
      }
    },
    title: {
      display: true,
      text: 'Distribuição de Veículos por Tipo' + (locationFilter.value !== 'Todos' ? ` - ${locationFilter.value}` : ''),
      font: {
        size: 16,
        weight: 'bold'
      },
      padding: {
        top: 10,
        bottom: 20
      }
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          const label = context.label.split(' (')[0] || '';
          const value = context.raw || 0;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = total ? Math.round((value / total) * 100) : 0;
          return `${label}: ${value} (${percentage}%)`;
        }
      }
    }
  },
  cutout: '60%',
  animation: {
    animateScale: true,
    animateRotate: true
  }
};
</script>

<template>
  <div>
    <div class="filter-container">
      <label class="filter-label">
        Localidade:
        <select v-model="locationFilter" class="filter-select">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>

      <label class="filter-label">
        Período:
        <select v-model="timeInterval" class="filter-select">
          <option value="dia">Hoje</option>
          <option value="semana">Última Semana</option>
          <option value="mes">Último Mês</option>
          <option value="ano">Último Ano</option>
          <option value="custom">Personalizado</option>
        </select>
      </label>

      <template v-if="timeInterval === 'custom'">
        <label class="filter-label">
          Data Início:
          <input 
            type="date" 
            v-model="dateRange.start" 
            class="filter-select"
          />
        </label>
        <label class="filter-label">
          Data Fim:
          <input 
            type="date" 
            v-model="dateRange.end" 
            class="filter-select"
          />
        </label>
      </template>
    </div>

    <div class="chart-container">
      <Pie :data="chartData" :options="chartOptions" />
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
  height: 450px;
  width: 100%;
  margin-top: 1rem;
}
</style>
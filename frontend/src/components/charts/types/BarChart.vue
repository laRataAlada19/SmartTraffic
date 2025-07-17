<script setup>
import { ref, computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  }
})

const locationFilter = ref('Todos')
const dateFrom = ref('')
const dateTo = ref('')

const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos']
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'))
  return ['Todos', ...unique]
})

const filteredData = computed(() => {
  if (!Array.isArray(props.data)) return []

  let filtered = [...props.data]

  if (locationFilter.value !== 'Todos') {
    filtered = filtered.filter(d => d.location === locationFilter.value)
  }

  if (dateFrom.value) {
    filtered = filtered.filter(d => d.full_date >= dateFrom.value)
  }

  if (dateTo.value) {
    filtered = filtered.filter(d => d.full_date <= dateTo.value)
  }

  return filtered
})

const chartData = computed(() => {
  const totals = {
    Carro: 0,
    Motociclo: 0,
    Bicicleta: 0,
    Camião: 0,
    Autocarro: 0,
  }

  filteredData.value.forEach(d => {
    totals.Carro += d.car || 0
    totals.Motociclo += d.motorcycle || 0
    totals.Bicicleta += d.bike || 0
    totals.Camião += d.truck || 0
    totals.Autocarro += d.bus || 0
  })

  const sortedEntries = Object.entries(totals).sort((a, b) => b[1] - a[1])
  return {
    labels: sortedEntries.map(e => e[0]),
    datasets: [{
      label: 'Total por Tipo de Veículo',
      data: sortedEntries.map(e => e[1]),
      backgroundColor: [
        '#36A2EB',
        '#FF6384',
        '#FFCE56',
        '#4BC0C0',
        '#9966FF',
      ],
      borderColor: '#444',
      borderWidth: 1,
      borderRadius: 5,
    }]
  }
})

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
    tooltip: {
      callbacks: {
        label(ctx) {
          const total = ctx.dataset.data.reduce((a,b) => a+b, 0)
          const val = ctx.parsed.y
          const percent = ((val / total) * 100).toFixed(1)
          return `${ctx.label}: ${val} (${percent}%)`
        }
      }
    }
  },
  scales: {
    x: {
      beginAtZero: true,
      title: { display: true, text: 'Tipo de Veículo' },
    },
    y: {
      beginAtZero: true,
      title: { display: true, text: 'Total de Veículos' },
      grid: { color: '#eee' },
    }
  },
  animation: { duration: 600 },
}
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
        Data Início:
        <input 
          type="date" 
          v-model="dateFrom" 
          class="filter-select"
        />
      </label>

      <label class="filter-label">
        Data Fim:
        <input 
          type="date" 
          v-model="dateTo" 
          class="filter-select"
        />
      </label>
    </div>

    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.filter-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-label {
  font-weight: 500;
  color: #fff;
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
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
</style>
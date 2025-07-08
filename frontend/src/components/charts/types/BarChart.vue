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
const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});
const selectedLocation = ref('all')
const dateFrom = ref('')
const dateTo = ref('')

// Filtrar dados por localização e datas
const filteredData = computed(() => {
  return props.data.filter(d => {
    const dateOk = (!dateFrom.value || d.full_date >= dateFrom.value) &&
                   (!dateTo.value || d.full_date <= dateTo.value)
    const locationOk = selectedLocation.value === 'all' || d.location === selectedLocation.value
    return dateOk && locationOk
  })
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

  // Ordenar por total desc
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
      borderRadius: 5, // bordas arredondadas nas barras
    }]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: true, position: 'top' },
    title: { display: true, text: 'Distribuição por Tipo de Veículo' },
    tooltip: {
      callbacks: {
        label(ctx) {
          const total = ctx.dataset.data.reduce((a,b) => a+b, 0)
          const val = ctx.parsed.y
          const percent = ((val / total) * 100).toFixed(1)
          return `${ctx.label}: ${val} (${percent}%)`
        }
      }
    },
    datalabels: { // se usares plugin chartjs-plugin-datalabels
      anchor: 'end',
      align: 'top',
      color: '#444',
      font: { weight: 'bold' },
      formatter: value => value,
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
  <div class="filters">
    <label class="filter-label">
        Localidade:
        <select v-model="locationFilter" class="filter-select">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>

    <label>
      Data Início:
      <input type="date" v-model="dateFrom" />
    </label>

    <label>
      Data Fim:
      <input type="date" v-model="dateTo" />
    </label>
  </div>

  <Bar :data="chartData" :options="chartOptions" />
</template>

<style scoped>
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}
.filters label {
  display: flex;
  flex-direction: column;
  font-weight: 500;
}
</style>

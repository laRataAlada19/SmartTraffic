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
  LinearScale
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
)

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
})

// Estados dos filtros
const selectedDay = ref('')
const selectedPeriod = ref('')

// Opções para os filtros (extrai dias e períodos únicos dos dados)
const availableDays = computed(() => {
  const days = [...new Set(props.data.map(item => item.day))]
  return days.sort((a, b) => a - b)
})

const availablePeriods = computed(() => {
  return [...new Set(props.data.map(item => item.period))]
})

// Filtra os dados com base nas seleções
const filteredData = computed(() => {
  if (!selectedDay.value && !selectedPeriod.value) return props.data

  return props.data.filter(item => {
    const matchesDay = !selectedDay.value || item.day === selectedDay.value
    const matchesPeriod = !selectedPeriod.value || item.period === selectedPeriod.value
    return matchesDay && matchesPeriod
  })
})

// Processa os dados para o gráfico
const chartData = computed(() => {
  const periods = {}
  
  filteredData.value.forEach(item => {
    const key = selectedDay.value 
      ? `Dia ${item.day} (${item.period})` 
      : item.period

    if (!periods[key]) {
      periods[key] = {
        Carro: 0,
        Motociclo: 0,
        Bicicleta: 0,
        Camião: 0,
        Autocarro: 0
      }
    }
    
    periods[key].Carro += item.car || 0
    periods[key].Motociclo += item.motorcycle || 0
    periods[key].Bicicleta += item.bike || 0
    periods[key].Camião += item.truck || 0
    periods[key].Autocarro += item.bus || 0
  })

  const periodLabels = Object.keys(periods)
  const vehicleTypes = ['Carro', 'Motociclo', 'Bicicleta', 'Camião', 'Autocarro']
  const colors = ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0', '#9966FF']

  return {
    labels: periodLabels,
    datasets: vehicleTypes.map((type, index) => ({
      label: type,
      data: periodLabels.map(period => periods[period][type]),
      backgroundColor: colors[index],
      borderColor: '#444',
      borderWidth: 1
    }))
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top'
    },
    title: {
      display: true,
      text: 'Comparação de Tráfego por Período'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: { display: true, text: 'Número de Veículos' }
    },
    x: {
      title: { display: true, text: 'Período' }
    }
  }
}
</script>

<template>
  <div class="filters">
    <select v-model="selectedDay">
      <option value="">Todos os dias</option>
      <option v-for="day in availableDays" :key="day" :value="day">
        Dia {{ day }}
      </option>
    </select>

    <select v-model="selectedPeriod">
      <option value="">Todos os períodos</option>
      <option v-for="period in availablePeriods" :key="period" :value="period">
        {{ period }}
      </option>
    </select>
  </div>

  <Bar 
    :data="chartData" 
    :options="chartOptions" 
  />
</template>

<style scoped>
.filters {
  margin-bottom: 20px;
}
select {
  margin-right: 10px;
  padding: 5px;
}
</style>
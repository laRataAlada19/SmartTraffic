<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import dayjs from 'dayjs'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement)

const store = useFactVehicleStore()
const locationFilter = ref('Todos')
const timeInterval = ref('dia')
const data1 = ref([])
const getVehicleDataByType = (type) => {
  const locationsSet = [...new Set(data1.value.map(d => d.location || 'Desconhecido'))]
  return locationsSet.map(loc => {
    const locEntries = data1.value.filter(d => d.location === loc)
    return locEntries.reduce((sum, entry) => sum + (entry[type] || 0), 0)
  })
}

onMounted(async () => {
  if (!Array.isArray(data1.value) || data1.value.length === 0) {
    data1.value = await store.fetchData()
    console.log('Dados carregados:', data1.value)
  }
})

const locations = computed(() => {
  if (!Array.isArray(data1.value)) return ['Todos']
  const unique = new Set(data1.value.map(entry => entry.location || 'Desconhecido'))
  return ['Todos', ...unique]
})

const filteredData = computed(() => {
  if (!Array.isArray(data1.value)) return []

  let data = [...data1.value]

  if (locationFilter.value !== 'Todos') {
    data = data.filter(d => d.location === locationFilter.value)
  }

  const grouped = {}

  data.forEach(entry => {
    let key = ''

    switch (timeInterval.value) {
      case 'mes':
        key = `${entry.year}-${String(entry.month).padStart(2, '0')}`
        break
      case 'semana':
        key = dayjs(entry.full_date).startOf('week').format('YYYY-MM-DD')
        break
      case 'dia':
      default:
        key = entry.full_date
    }

    if (!grouped[key]) grouped[key] = 0
    grouped[key] += entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus
  })

  return Object.entries(grouped).sort((a, b) => new Date(a[0]) - new Date(b[0]))
})
</script>

<template>
  <div>
    <div style="margin-bottom: 1rem;">
      <label>Localidade:
        <select v-model="locationFilter">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>

      <label style="margin-left: 2rem;">Intervalo:
        <select v-model="timeInterval">
          <option value="dia">Dia</option>
          <option value="semana">Semana</option>
          <option value="mes">Mês</option>
        </select>
      </label>
    </div>

    <Bar
  v-if="data1.length"
  :data="{
    labels: [...new Set(data1.map(d => d.location || 'Desconhecido'))],
    datasets: [
      {
        label: 'Carros',
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        data: getVehicleDataByType('car')
      },
      {
        label: 'Motas',
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
        data: getVehicleDataByType('motorcycle')
      },
      {
        label: 'Camiões',
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
        data: getVehicleDataByType('truck')
      },
      {
        label: 'Autocarros',
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
        data: getVehicleDataByType('bus')
      }
    ]
  }"
  :options="{
    responsive: true,
    plugins: {
      legend: { display: true },
      title: { display: true, text: 'Tipos de Veículo por Localidade' }
    },
    scales: {
      y: { beginAtZero: true },
      x: { stacked: true },
      yAxes: [{ stacked: true }]
    }
  }"
/>

    <p v-else>Nenhum dado disponível.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'
import { useFactVehicleStore  } from '@/stores/factvehicle'
import dayjs from 'dayjs'
import { useSharedData } from '@/components/charts/useSharedData';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const store = useFactVehicleStore()
const locationFilter = ref('Todos')
const timeInterval = ref('dia')
const data1 = ref([])
const { sharedData } = useSharedData();



onMounted(async () => {
  if (!Array.isArray(data1.value) || data1.value.length === 0) {
    data1.value= sharedData.value;
    console.log('Dados carregados kbjhasvdjahvfsghvdsjcbdshkbcsdbc:', data1.value)
    
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

    <Line
      v-if="filteredData.length"
      :data="{
        labels: filteredData.map(d => d[0]),
        datasets: [{
          label: 'Total de Veículos',
          data: filteredData.map(d => d[1]),
          borderColor: 'rgb(75, 192, 192)',
          fill: false,
          tension: 0.1
        }]
      }"
      :options="{
        responsive: true,
        plugins: {
          legend: { display: true },
          title: { display: true, text: 'Contagem de Veículos' }
        }
      }"
    />
    <p v-else>Nenhum dado disponível.</p>
  </div>
</template>


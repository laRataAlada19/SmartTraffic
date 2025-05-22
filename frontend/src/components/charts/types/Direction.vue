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
  LinearScale
} from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import dayjs from 'dayjs'

ChartJS.register(
  Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale
)

const store = useFactVehicleStore()
const locationFilter = ref('Todos')
const timeInterval = ref('dia')
const data1 = ref([])

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

const directionData = computed(() => {
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

    if (!grouped[key]) {
      grouped[key] = {
        norte: entry.n + entry.ne + entry.nw,
        sul: entry.s + entry.se + entry.sw,
        leste: entry.e + entry.ne + entry.se,
        oeste: entry.w + entry.nw + entry.sw
      }
    } else {
      grouped[key].norte += entry.n + entry.ne + entry.nw
      grouped[key].sul += entry.s + entry.se + entry.sw
      grouped[key].leste += entry.e + entry.ne + entry.se
      grouped[key].oeste += entry.w + entry.nw + entry.sw
    }
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

    <div style="margin-top: 2rem;">
      <h2>Direções do Tráfego</h2>
      <Bar
        v-if="directionData.length"
        :data="{
          labels: directionData.map(d => d[0]),
          datasets: [
            {
              label: 'Norte',
              data: directionData.map(d => d[1].norte),
              backgroundColor: 'rgba(41, 128, 185, 0.7)',
              borderColor: 'rgba(41, 128, 185, 1)',
              borderWidth: 1
            },
            {
              label: 'Sul',
              data: directionData.map(d => d[1].sul),
              backgroundColor: 'rgba(231, 76, 60, 0.7)',
              borderColor: 'rgba(231, 76, 60, 1)',
              borderWidth: 1
            },
            {
              label: 'Leste',
              data: directionData.map(d => d[1].leste),
              backgroundColor: 'rgba(39, 174, 96, 0.7)',
              borderColor: 'rgba(39, 174, 96, 1)',
              borderWidth: 1
            },
            {
              label: 'Oeste',
              data: directionData.map(d => d[1].oeste),
              backgroundColor: 'rgba(243, 156, 18, 0.7)',
              borderColor: 'rgba(243, 156, 18, 1)',
              borderWidth: 1
            }
          ]
        }"
        :options="{
          responsive: true,
          plugins: {
            legend: { 
              display: true,
              position: 'top'
            },
            title: { 
              display: true,
              text: 'Fluxo de Tráfego por Direção Cardinal',
              font: {
                size: 16
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false
            }
          },
          scales: {
            y: { 
              beginAtZero: true,
              title: {
                display: true,
                text: 'Quantidade de Veículos'
              }
            },
            x: { 
              title: {
                display: true,
                text: 'Período'
              }
            }
          },
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
          }
        }"
      />
      <p v-else style="color: #666; font-style: italic;">
        Nenhum dado disponível para os filtros selecionados.
      </p>
    </div>
  </div>
</template>

<style scoped>
div {
  font-family: Arial, sans-serif;
}
label {
  font-weight: bold;
}
select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-left: 5px;
}
h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}
</style>
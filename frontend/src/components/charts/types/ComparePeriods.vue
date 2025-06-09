<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import dayjs from 'dayjs'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const store = useFactVehicleStore()
const data = ref([])
const start1 = ref('2025-05-21')
const start2 = ref('2025-05-20')

onMounted(async () => {
    console.log("Fetching data for ComparePeriods chart")
  data.value = await store.fetchData()
})

function getTotalsByDate(date) {
  const filtered = data.value.filter(d => d.full_date === date)
  return ['car', 'motorcycle', 'bike', 'truck', 'bus'].map(type =>
    filtered.reduce((sum, d) => sum + (d[type] || 0), 0)
  )
}
</script>

<template>
  <div>
    <label>Data 1: <input type="date" v-model="start1" /></label>
    <label style="margin-left: 1rem;">Data 2: <input type="date" v-model="start2" /></label>

    <Bar :data="{
      labels: ['Carro', 'Moto', 'Bicicleta', 'Camião', 'Autocarro'],
      datasets: [
        {
          label: `Dia ${start1}`,
          data: getTotalsByDate(start1),
          backgroundColor: 'rgba(75, 192, 192, 0.6)'
        },
        {
          label: `Dia ${start2}`,
          data: getTotalsByDate(start2),
          backgroundColor: 'rgba(255, 99, 132, 0.6)'
        }
      ]
    }" :options="{ responsive: true }" />
  </div>
</template>

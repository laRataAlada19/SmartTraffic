<script setup>
import { ref, onMounted, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale)

const store = useFactVehicleStore()
const data = ref([])

onMounted(async () => {
  data.value = await store.fetchData()
  console.log("Trend data fetched:", data.value)
})

const days = computed(() => {
  const grouped = {}
  data.value.forEach(d => {
    grouped[d.full_date] ??= 0
    grouped[d.full_date] += d.car + d.motorcycle + d.bike + d.truck + d.bus
  })
  return Object.entries(grouped)
})
</script>

<template>
  <Line :data="{
    labels: days.map(([d]) => d),
    datasets: [{
      label: 'Total de veículos por dia',
      data: days.map(([_, v]) => v),
      borderColor: 'purple',
      fill: false
    }]
  }" :options="{ responsive: true }" />
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import { useSharedData } from '@/components/charts/useSharedData';

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale)

const store = useFactVehicleStore()
const data = ref([])
const { sharedData } = useSharedData();


onMounted(async () => {
  data.value = sharedData.value;
    console.log("Direction Radar data fetched:", data.value)
})

const minutes = data.value.map(d => `${d.hour}:${String(d.minute).padStart(2, '0')}`)
const totals = data.value.map(d => d.car + d.motorcycle + d.bike + d.truck + d.bus)
</script>

<template>
  <Line :data="{
    labels: minutes,
    datasets: [{
      label: 'Veículos por minuto',
      data: totals,
      borderColor: 'blue',
      fill: false
    }]
  }" :options="{ responsive: true }" />
</template>

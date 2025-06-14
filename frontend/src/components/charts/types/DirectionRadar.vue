<script setup>
import { ref, onMounted } from 'vue'
import { Radar } from 'vue-chartjs'
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend } from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import { useSharedData } from '@/components/charts/useSharedData';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend)

const store = useFactVehicleStore()
const data = ref([])
const { sharedData } = useSharedData();


onMounted(async () => {
  data.value = sharedData.value;
    console.log("Direction Radar data fetched:", data.value)
})

const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
const totalByDir = directions.map(dir =>
  data.value.reduce((sum, d) => sum + (d[dir] || 0), 0)
)
</script>

<template>
  <Radar :data="{
    labels: ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
    datasets: [{
      label: 'Direção de tráfego',
      data: totalByDir,
      backgroundColor: 'rgba(255, 206, 86, 0.2)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 2
    }]
  }" :options="{ responsive: true }" />
</template>

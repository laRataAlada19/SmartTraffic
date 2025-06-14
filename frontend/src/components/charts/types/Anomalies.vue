<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js'

import { useSharedData } from '@/components/charts/useSharedData';


ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale)


const data = ref([])
const { sharedData } = useSharedData();

onMounted(async () => {
  data.value = sharedData.value;
  console.log("Anomalies data fetched:", data.value)
})

const totals = data.value.map(d => d.car + d.motorcycle + d.bike + d.truck + d.bus)
const labels = data.value.map(d => `${d.hour}:${d.minute}`)
const avg = totals.reduce((a, b) => a + b, 0) / totals.length
const anomalyIndices = totals.map((val, i) => (val > avg * 1.5 ? val : null))
</script>

<template>
  <Line :data="{
    labels,
    datasets: [
      {
        label: 'Tráfego',
        data: totals,
        borderColor: 'blue',
        fill: false
      },
      {
        label: 'Anomalias',
        data: anomalyIndices,
        borderColor: 'red',
        pointBackgroundColor: 'red',
        showLine: false
      }
    ]
  }" :options="{ responsive: true }" />
</template>

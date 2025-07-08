<script setup>
import { ref, onMounted, computed } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Title } from 'chart.js'
import dayjs from 'dayjs'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend, Title)

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
})

const data = ref([])

onMounted(() => {
  data.value = props.data
})

const days = computed(() => {
  const grouped = {}
  data.value.forEach(d => {
    grouped[d.full_date] ??= 0
    grouped[d.full_date] += d.car + d.motorcycle + d.bike + d.truck + d.bus
  })
  return Object.entries(grouped)
    .sort((a, b) => new Date(a[0]) - new Date(b[0]))
    .map(([date, total]) => [dayjs(date).format('DD/MM'), total])
})

const options = {
  responsive: true,
  plugins: {
    legend: {
      display: true,
      position: 'top',
    },
    title: {
      display: true,
      text: 'Tendência Diária de Tráfego',
      font: { size: 18 }
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      callbacks: {
        label: ctx => `Veículos: ${ctx.parsed.y}`,
      }
    },
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false,
  },
  scales: {
    x: {
      title: { display: true, text: 'Data' },
      ticks: { maxRotation: 45, minRotation: 45, maxTicksLimit: 10 },
      grid: { display: false }
    },
    y: {
      title: { display: true, text: 'Número de Veículos' },
      beginAtZero: true,
      grid: { color: '#eee' }
    }
  },
  elements: {
    line: { tension: 0.3, borderWidth: 2 },
    point: { radius: 3, hoverRadius: 6 }
  }
}
</script>

<template>
  <Line
    :data="{
      labels: days.map(([d]) => d),
      datasets: [{
        label: 'Total de veículos por dia',
        data: days.map(([_, v]) => v),
        borderColor: 'purple',
        fill: false,
      }]
    }"
    :options="options"
  />
</template>

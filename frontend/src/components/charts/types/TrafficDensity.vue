<script setup>
import { ref, computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Tooltip,
  Legend
} from 'chart.js'
import dayjs from 'dayjs'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Legend)

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
})

const selectedDate = ref(dayjs().format('YYYY-MM-DD'))

const selectedTypes = ref({
  all: true,
  car: true,
  motorcycle: true,
  bike: true,
  truck: true,
  bus: true,
})

const colors = {
  all: '#555',
  car: '#ff6384',
  motorcycle: '#36a2eb',
  bike: '#ffce56',
  truck: '#4bc0c0',
  bus: '#9966ff',
}

const labels = {
  all: 'Todos',
  car: 'Carros',
  motorcycle: 'Motas',
  bike: 'Bicicletas',
  truck: 'Camiões',
  bus: 'Autocarros',
}

const allSelected = computed(() =>
  Object.values(selectedTypes.value).every(v => v === true)
)

const toggleAll = () => {
  const newState = !allSelected.value
  Object.keys(selectedTypes.value).forEach(type => {
    selectedTypes.value[type] = newState
  })
}

const toggleType = type => {
  selectedTypes.value[type] = !selectedTypes.value[type]
}

const filteredData = computed(() =>
  props.data.filter(entry => entry.full_date === selectedDate.value)
)

const chartData = computed(() => {
  const datasets = []
  

  Object.keys(selectedTypes.value).forEach(type => {
    console.log("aquiii" + selectedTypes.value[type])
    if (selectedTypes.value[type] && type !== 'all') {
      datasets.push({
        label: labels[type],
        data: filteredData.value.map(d => d[type]),
        borderColor: colors[type],
        fill: false,
        tension: 0.3,
      })
    }
    if (type === 'all' && allSelected.value) {
      datasets.push({
        label: labels[type],
        data: filteredData.value.map(d => d.car + d.motorcycle + d.bike + d.truck + d.bus),
        borderColor: colors[type],
        fill: false,
        tension: 0.3,
      })
    }
  })

  return {
    labels: filteredData.value.map(d => `${d.hour}:${String(d.minute).padStart(2, '0')}`),
    datasets,
  }
})
</script>

<template>
  <div>
    <div class="filter-bar">
      <label>
        Escolher dia:
        <input type="date" v-model="selectedDate" class="date-picker" />
      </label>
    </div>
    <Line :data="chartData" :options="{ responsive: true, plugins: { legend: { display: true } } }" />
  </div>
</template>

<style scoped>
.filter-bar {
  margin-bottom: 1rem;
}

.date-picker {
  margin-left: 0.5rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #fff;
  color: #333;
}

.vehicle-type-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.vehicle-box {
  padding: 0.4rem 0.8rem;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 500;
  user-select: none;
  transition: all 0.2s ease;
  min-width: 100px;
  text-align: center;
}

.all-box {
  background-color: #555;
  border: 2px solid #444;
}
</style>

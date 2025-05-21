<script setup>
import { ref, computed, onMounted } from 'vue'
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import dayjs from 'dayjs'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

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

const aggregatedVehicleCounts = computed(() => {
  if (!Array.isArray(data1.value)) return {}

  let data = [...data1.value]

  if (locationFilter.value !== 'Todos') {
    data = data.filter(d => d.location === locationFilter.value)
  }

  // Podemos ignorar o timeInterval para o total geral, ou se quiseres, podes filtrar por intervalo também.
  // Aqui vamos pegar em todos os dados filtrados pela localização e somar os veículos de cada tipo

  const totals = {
    car: 0,
    motorcycle: 0,
    bike: 0,
    truck: 0,
    bus: 0
  }

  data.forEach(entry => {
    totals.car += entry.car
    totals.motorcycle += entry.motorcycle
    totals.bike += entry.bike
    totals.truck += entry.truck
    totals.bus += entry.bus
  })

  return totals
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

    <Pie
      v-if="Object.values(aggregatedVehicleCounts).some(val => val > 0)"
      :data="{
        labels: ['Veiculo Ligeiro', 'Motociclo', 'Bicicletas', 'Camiões', 'Autocarros'],
        datasets: [{
          label: 'Distribuição de Veículos',
          data: [
            aggregatedVehicleCounts.car,
            aggregatedVehicleCounts.motorcycle,
            aggregatedVehicleCounts.bike,
            aggregatedVehicleCounts.truck,
            aggregatedVehicleCounts.bus
          ],
          backgroundColor: [
            'rgba(75, 192, 192, 0.7)',
            'rgba(255, 159, 64, 0.7)',
            'rgba(153, 102, 255, 0.7)',
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)'
          ],
          borderColor: 'white',
          borderWidth: 2
        }]
      }"
      :options="{
        responsive: true,
        plugins: {
          legend: { position: 'right' },
          title: { display: true, text: 'Distribuição de Veículos por Tipo' }
        }
      }"
    />
    <p v-else>Nenhum dado disponível para mostrar o gráfico de pizza.</p>
  </div>
</template>

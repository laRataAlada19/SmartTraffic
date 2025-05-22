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
  LinearScale,
  PointElement
} from 'chart.js'
import { useFactVehicleStore } from '@/stores/factvehicle'
import dayjs from 'dayjs'


ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);
ChartJS.register(BarElement) 
const data1 = ref([]); 
const locationFilter = ref('Todos');
const timeInterval = ref('dia'); 

onMounted(async () => {
  const store = useFactVehicleStore(); 
  data1.value = await store.fetchData(); 
  console.log('Dados carregados:', data1.value);
});

const vehicleTypeData = computed(() => {
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
        car: 0,
        motorcycle: 0,
        bike: 0,
        truck: 0,
        bus: 0
      }
    }

    grouped[key].car += entry.car
    grouped[key].motorcycle += entry.motorcycle
    grouped[key].bike += entry.bike
    grouped[key].truck += entry.truck
    grouped[key].bus += entry.bus
  })

  return Object.entries(grouped).sort((a, b) => new Date(a[0]) - new Date(b[0]))
})
</script>

<template>
  <div>
    <div style="margin-top: 3rem;">
      <Bar
        v-if="vehicleTypeData.length"
        :data="{
          labels: vehicleTypeData.map(d => d[0]),
          datasets: [
            {
              label: 'Carros',
              data: vehicleTypeData.map(d => d[1].car),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            },
            {
              label: 'Motocicletas',
              data: vehicleTypeData.map(d => d[1].motorcycle),
              backgroundColor: 'rgba(255, 99, 132, 0.5)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            },
            {
              label: 'Bicicletas',
              data: vehicleTypeData.map(d => d[1].bike),
              backgroundColor: 'rgba(75, 192, 192, 0.5)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            },
            {
              label: 'Caminhões',
              data: vehicleTypeData.map(d => d[1].truck),
              backgroundColor: 'rgba(255, 206, 86, 0.5)',
              borderColor: 'rgba(255, 206, 86, 1)',
              borderWidth: 1
            },
            {
              label: 'Ônibus',
              data: vehicleTypeData.map(d => d[1].bus),
              backgroundColor: 'rgba(153, 102, 255, 0.5)',
              borderColor: 'rgba(153, 102, 255, 1)',
              borderWidth: 1
            }
          ]
        }"
        :options="{
          responsive: true,
          plugins: {
            legend: { display: true },
            title: { display: true, text: 'Distribuição de Tipos de Veículos' }
          },
          scales: {
            y: { beginAtZero: true, stacked: false },
            x: { stacked: false }
          }
        }"
      />
      <p v-else>Nenhum dado disponível para tipos de veículos.</p>
    </div>
  </div>
</template>
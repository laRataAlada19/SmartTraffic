<template>
    <div class="od-matrix">
      <h3>Matriz Origem-Destino</h3>
      <table>
        <thead>
          <tr>
            <th>Origem \ Destino</th>
            <th v-for="dest in locations" :key="dest">{{ dest }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="origin in locations" :key="origin">
            <th>{{ origin }}</th>
            <td v-for="dest in locations" :key="dest"
                :style="{ backgroundColor: getColor(matrix[origin]?.[dest] || 0) }">
              {{ matrix[origin]?.[dest] || 0 }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useFactVehicleStore } from '@/stores/factvehicle'
  import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet';
  const store = useFactVehicleStore()
  const data = ref([])
  
  onMounted(async () => {
    data.value = await store.fetchData()
  })
  
  // Assume que cada entrada tem: { location, destination }
  const locations = Array.from(new Set(data.value.flatMap(d => [d.location, d.destination])))
  
  const matrix = locations.reduce((acc, origin) => {
    acc[origin] = {}
    locations.forEach(dest => acc[origin][dest] = 0)
    return acc
  }, {})
  
  data.value.forEach(entry => {
    if (entry.location && entry.destination) {
      matrix[entry.location][entry.destination] +=
        entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus
    }
  })
  
  function getColor(value) {
    const max = 100 // define valor máximo esperado
    const opacity = Math.min(1, value / max)
    return `rgba(0, 123, 255, ${opacity})`
  }
  </script>
  
  <style scoped>
  .od-matrix table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
  }
  .od-matrix th, .od-matrix td {
    border: 1px solid #ccc;
    padding: 6px;
  }
  </style>
  
<template>
    <div style="height: 500px;">
      <l-map :zoom="14" :center="center" style="height: 100%;">
        <l-tile-layer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors" />
        <l-circle-marker
          v-for="(entry, i) in filteredData"
          :key="i"
          :lat-lng="[entry.latitude, entry.longitude]"
          :radius="5"
          :color="'blue'"
          :fill="true"
          fill-opacity="0.6"
        >
          <l-popup>
            <p><strong>{{ entry.full_date }} {{ entry.hour }}:{{ entry.minute }}</strong></p>
            <p>Total: {{ total(entry) }}</p>
          </l-popup>
        </l-circle-marker>
      </l-map>
  
      <div class="mt-4">
        <label>Hora:
          <input type="range" min="0" max="23" v-model="selectedHour" />
          {{ selectedHour }}h
        </label>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useFactVehicleStore } from '@/stores/factvehicle'
  import { LMap, LTileLayer, LCircleMarker, LPopup } from '@vue-leaflet/vue-leaflet'

  const center = ref([39.748, -8.807]) // Leiria como default
  const selectedHour = ref(12)
  const data = ref([])
  
  const store = useFactVehicleStore()
  onMounted(async () => {
    data.value = await store.fetchData()
  })
  
  const filteredData = computed(() =>
    data.value.filter(d => Number(d.hour) === selectedHour.value)
  )
  
  const total = entry =>
    entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus
  </script>
  
  <style>
  .l-map {
    border: 1px solid #ccc;
    border-radius: 8px;
  }
  </style>
  
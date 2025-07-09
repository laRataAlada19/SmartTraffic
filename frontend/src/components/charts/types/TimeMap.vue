<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { LMap, LTileLayer, LCircleMarker, LPopup } from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';
import dayjs from 'dayjs';

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
});


// Estado
const center = ref([39.748, -8.807]); // Leiria
const zoom = ref(13);
const selectedHour = ref(new Date().getHours());
const locationFilter = ref('Todos');
const timeInterval = ref('dia');

// Lista de localidades únicas
const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

// Agrupamento por intervalo temporal
const groupData = computed(() => {
  const filtered = props.data.filter(d => {
    const hour = parseInt(d.hour);
    return (
      (locationFilter.value === 'Todos' || d.location === locationFilter.value) &&
      hour === selectedHour.value
    );
  });

  const grouped = {};
  for (const entry of filtered) {
    const key = `${entry.latitude},${entry.longitude}`;
    if (!grouped[key]) {
      grouped[key] = {
        id: key,
        latitude: parseFloat(entry.latitude),
        longitude: parseFloat(entry.longitude),
        location: entry.location,
        hour: entry.hour,
        total: 0,
        car: 0,
        truck: 0,
        motorcycle: 0,
        bus: 0,
        bike: 0,
      };
    }

    grouped[key].car += Number(entry.car) || 0;
    grouped[key].motorcycle += Number(entry.motorcycle) || 0;
    grouped[key].truck += Number(entry.truck) || 0;
    grouped[key].bus += Number(entry.bus) || 0;
    grouped[key].bike += Number(entry.bike) || 0;
  }

  return Object.values(grouped);
});


// Cálculo do total e cor dominante
const filteredData = computed(() =>
  groupData.value.map(entry => ({
    ...entry,
    total: (entry.car || 0) +
           (entry.motorcycle || 0) +
           (entry.bike || 0) +
           (entry.truck || 0) +
           (entry.bus || 0),
  }))
);

const getColor = (entry) => {
  const maxType = Math.max(
    entry.car || 0,
    entry.motorcycle || 0,
    entry.bike || 0,
    entry.truck || 0,
    entry.bus || 0
  );

  if (maxType === entry.car) return '#36A2EB';
  if (maxType === entry.motorcycle) return '#FF6384';
  if (maxType === entry.bike) return '#FFCE56';
  if (maxType === entry.truck) return '#4BC0C0';
  return '#9966FF';
};

// Ajusta centro ao primeiro ponto visível
watch(filteredData, data => {
  console.log('Raw Data:', props.data);

  if (data.length > 0) {
    center.value = [data[0].latitude, data[0].longitude];
  }
});
</script>
<template>
  <div class="p-4 bg-slate-800 rounded-xl shadow-md text-white">
    <h2 class="text-lg font-semibold mb-1">Mapa com evolução temporal</h2>
    <p class="text-sm text-slate-300 mb-4">Mapa que mostra a evolução dos dados ao longo do tempo.</p>

    <div class="bg-slate-700 p-4 rounded-lg">
      <h3 class="text-md font-semibold mb-2">Evolução Temporal do Tráfego</h3>

      <!-- Filtros -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm mb-1">Localidade:</label>
          <select v-model="locationFilter" class="w-full rounded-md px-2 py-1 bg-white text-black">
            <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
          </select>
        </div>

        <div>
          <label class="block text-sm mb-1">Intervalo:</label>
          <select v-model="timeInterval" class="w-full rounded-md px-2 py-1 bg-white text-black">
            <option value="dia">Dia</option>
            <option value="semana">Semana</option>
            <option value="mes">Mês</option>
          </select>
        </div>

        <div>
          <label class="block text-sm mb-1">
  Hora: {{ selectedHour.toString().padStart(2, '0') }}:00
</label>

<input type="range" min="0" max="23" v-model.number="selectedHour" class="w-full accent-blue-500">

        </div>
      </div>

      <!-- Mapa -->
      <LMap
        :zoom="zoom"
        :center="center"
        class="h-96 rounded-lg overflow-hidden z-10"
        @update:zoom="newZoom => zoom = newZoom"
        @update:center="newCenter => center = newCenter"
      >
        <LTileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        />

        <LCircleMarker
          v-for="entry in filteredData"
          :key="entry.id"
          :lat-lng="[entry.latitude, entry.longitude]"
          :radius="Math.min(Math.sqrt(entry.total) * 2, 20)"
          :color="getColor(entry)"
          :fill-opacity="0.8"
          :weight="1"
        >
          <LPopup>
            <div class="text-sm">
              <strong>{{ entry.location }}</strong><br>
              Hora: {{ entry.hour }}:00<br>
              Total: {{ entry.total }} veículos<br>
              🚗 Carros: {{ entry.car || 0 }}<br>
              🏍️ Motos: {{ entry.motorcycle || 0 }}<br>
              🚲 Bicicletas: {{ entry.bike || 0 }}<br>
              🚛 Caminhões: {{ entry.truck || 0 }}<br>
              🚌 Ônibus: {{ entry.bus || 0 }}
            </div>
          </LPopup>
        </LCircleMarker>
      </LMap>
    </div>
  </div>
</template>



<script setup>
import { ref, computed, onMounted } from 'vue';
import { LMap, LTileLayer, LCircleMarker, LPopup, LControl } from '@vue-leaflet/vue-leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

// Configuração do mapa
const center = ref([39.748, -8.807]); // Centro em Leiria
const zoom = ref(13);
const selectedHour = ref(new Date().getHours()); // Hora atual como padrão

// Processamento dos dados
const filteredData = computed(() => {
  return props.data
    .filter(d => Number(d.hour) === selectedHour.value)
    .map(entry => ({
      ...entry,
      total: (entry.car || 0) + 
            (entry.motorcycle || 0) + 
            (entry.bike || 0) + 
            (entry.truck || 0) + 
            (entry.bus || 0)
    }));
});

// Cores baseadas no tipo de veículo predominante
const getColor = (entry) => {
  const maxType = Math.max(
    entry.car || 0,
    entry.motorcycle || 0,
    entry.bike || 0,
    entry.truck || 0,
    entry.bus || 0
  );
  
  if (maxType === entry.car) return '#36A2EB'; // Azul para carros
  if (maxType === entry.motorcycle) return '#FF6384'; // Vermelho para motos
  if (maxType === entry.bike) return '#FFCE56'; // Amarelo para bicicletas
  if (maxType === entry.truck) return '#4BC0C0'; // Ciano para caminhões
  return '#9966FF'; // Roxo para ônibus
};

// Ajusta o mapa quando os dados mudam
onMounted(() => {
  if (props.data.length > 0 && props.data[0].latitude) {
    center.value = [props.data[0].latitude, props.data[0].longitude];
  }
});
</script>

<template>
  <div class="time-map-container">
    <div class="time-controls">
      <h3>Evolução Temporal do Tráfego</h3>
      <div class="slider-container">
        <label>
          Hora: {{ selectedHour.toString().padStart(2, '0') }}:00
          <input 
            type="range" 
            min="0" 
            max="23" 
            v-model="selectedHour" 
            class="hour-slider"
          />
        </label>
      </div>
    </div>

    <LMap 
      :zoom="zoom" 
      :center="center" 
      class="leaflet-map"
      @update:zoom="newZoom => zoom = newZoom"
      @update:center="newCenter => center = newCenter"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
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
          <div class="popup-content">
            <h4>{{ entry.location }}</h4>
            <p><strong>Hora:</strong> {{ entry.hour }}:00</p>
            <p><strong>Total:</strong> {{ entry.total }} veículos</p>
            <div class="vehicle-details">
              <p>🚗 Carros: {{ entry.car || 0 }}</p>
              <p>🏍️ Motos: {{ entry.motorcycle || 0 }}</p>
              <p>🚲 Bicicletas: {{ entry.bike || 0 }}</p>
              <p>🚛 Caminhões: {{ entry.truck || 0 }}</p>
              <p>🚌 Ônibus: {{ entry.bus || 0 }}</p>
            </div>
          </div>
        </LPopup>
      </LCircleMarker>
    </LMap>
  </div>
</template>

<style scoped>
.time-map-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.leaflet-map {
  height: 500px;
  width: 100%;
  border-radius: 8px;
  border: 1px solid #ddd;
  z-index: 0;
}

.time-controls {
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.hour-slider {
  width: 300px;
  margin-left: 1rem;
}

.popup-content {
  min-width: 200px;
}

.vehicle-details {
  margin-top: 0.5rem;
  border-top: 1px solid #eee;
  padding-top: 0.5rem;
}

.vehicle-details p {
  margin: 0.2rem 0;
  font-size: 0.9rem;
}
</style>
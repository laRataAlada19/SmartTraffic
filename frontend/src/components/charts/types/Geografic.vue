<script setup>
import { ref, computed, onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const mapContainer = ref(null);
const map = ref(null);
const geoJsonLayer = ref(null);
const loading = ref(true);
const error = ref(null);

// Cores para o gradiente do mapa
const getColor = (value, maxValue) => {
  const ratio = value / maxValue;
  return ratio > 0.75 ? '#800026' :
         ratio > 0.5  ? '#BD0026' :
         ratio > 0.25 ? '#E31A1C' :
         ratio > 0.1  ? '#FC4E2A' :
         ratio > 0    ? '#FD8D3C' :
                        '#FFEDA0';
};

const styleFeature = (feature, maxValue) => {
  return {
    fillColor: getColor(feature.properties.value || 0, maxValue),
    weight: 1,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.7
  };
};

onMounted(async () => {
  try {
    // Carrega o GeoJSON dos distritos de Portugal
    const response = await fetch('https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries-10m.json');
    const worldData = await response.json();
    
    // Filtra apenas Portugal (precisa de ajuste para distritos)
    // NOTA: Este exemplo usa países, você precisará substituir por um GeoJSON de distritos portugueses
    const portugalData = {
      type: 'FeatureCollection',
      features: worldData.features.filter(f => f.properties.name === 'Portugal')
    };
    
    // Processa os dados de tráfego
    const maxValue = Math.max(...props.data.map(item => item.value || 0), 1);
    
    // Cria o mapa
    map.value = L.map(mapContainer.value).setView([39.3999, -8.2245], 6);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map.value);
    
    // Adiciona os dados GeoJSON com estilo
    geoJsonLayer.value = L.geoJSON(portugalData, {
      style: (feature) => styleFeature(feature, maxValue),
      onEachFeature: (feature, layer) => {
        const districtData = props.data.find(d => d.district === feature.properties.name);
        if (districtData) {
          layer.bindPopup(`
            <b>${feature.properties.name}</b><br>
            Tráfego total: ${districtData.value} veículos
          `);
        }
      }
    }).addTo(map.value);
    
    loading.value = false;
  } catch (err) {
    console.error('Erro ao carregar mapa:', err);
    error.value = 'Erro ao carregar o mapa. Por favor, tente novamente.';
    loading.value = false;
  }
});
</script>

<template>
  <div class="map-container">
    <h3>Mapa Geográfico de Tráfego em Portugal</h3>
    <div v-if="loading" class="loading-message">
      Carregando mapa...
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
    </div>
    <div v-else ref="mapContainer" class="map"></div>
  </div>
</template>

<style scoped>
.map-container {
  width: 100%;
  height: 600px;
  position: relative;
}

.map {
  width: 100%;
  height: 100%;
  background: #f0f0f0;
}

.loading-message, .error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background: white;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.error-message {
  color: #d32f2f;
}
</style>
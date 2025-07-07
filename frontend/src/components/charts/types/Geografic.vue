<template>
  <div class="h-[500px] w-full">
    <LMap
      :zoom="13"
      :center="[defaultLat, defaultLng]"
      style="height: 100%; width: 100%"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />

      <LMarker
        v-for="(item, index) in props.data"
        :key="index"
        :lat-lng="[item.latitude, item.longitude]"
        :icon="getIcon(item)"
      >
        <LPopup>
          <div>
            <p><strong>Localidade:</strong> {{ item.location }}</p>
            <p>Carros: {{ item.car }}</p>
            <p>Motociclos: {{ item.motorcycle }}</p>
            <p>Bicicletas: {{ item.bike }}</p>
            <p>Camiões: {{ item.truck }}</p>
            <p>Autocarros: {{ item.bus }}</p>
          </div>
        </LPopup>
      </LMarker>
    </LMap>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { LMap, LTileLayer, LMarker, LPopup } from 'vue-leaflet';
import L from 'leaflet'
import 'leaflet/dist/leaflet.css';

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
})

// Ícones por tipo de veículo mais dominante
function getIcon(item) {
  const maxType = getDominantType(item)
  const color = typeColors[maxType] || 'gray'

  return L.divIcon({
    className: 'custom-icon',
    html: `<div style="background:${color};width:14px;height:14px;border-radius:50%;border:2px solid white;"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  })
}

const typeColors = {
  car: '#36A2EB',
  motorcycle: '#FF6384',
  bike: '#FFCE56',
  truck: '#4BC0C0',
  bus: '#9966FF',
}

// Determinar o tipo de veículo mais dominante na localização
function getDominantType(item) {
  const entries = [
    ['car', item.car],
    ['motorcycle', item.motorcycle],
    ['bike', item.bike],
    ['truck', item.truck],
    ['bus', item.bus],
  ]
  return entries.reduce((max, curr) => (curr[1] > max[1] ? curr : max))[0]
}

// Coordenadas centrais (ajustáveis)
const defaultLat = 39.75 // Leiria?
const defaultLng = -8.8
</script>

<style scoped>
/* Opcional: remover ícones padrão dos marcadores */
.custom-icon {
  background: none !important;
  border: none !important;
}
</style>

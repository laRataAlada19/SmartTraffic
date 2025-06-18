<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/TimeMap.vue
import { ref, computed } from 'vue';
import { LMap, LTileLayer, LCircleMarker, LPopup  } from '@vue-leaflet/vue-leaflet';

// Accept the preloaded data as a prop
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const center = ref([39.748, -8.807]); // Default center (Leiria)
const selectedHour = ref(12);

const filteredData = computed(() =>
  props.data.filter(d => Number(d.hour) === selectedHour.value)
);

const total = entry =>
  entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus;
</script>

<template>
  <div>
    <div style="margin-bottom: 1rem;">
      <label>Hora:
        <input type="range" min="0" max="23" v-model="selectedHour" />
        {{ selectedHour }}h
      </label>
    </div>

    <LMap :zoom="13" :center="center" class="l-map" style="height: 500px;">
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      <LCircleMarker
        v-for="entry in filteredData" 
        :key="entry.id"
        :lat-lng="[entry.latitude, entry.longitude]"
        :radius="Math.min(total(entry) / 10, 20)"
        color="blue"
      >
        <LPopup>
          <div>
            <p><strong>Local:</strong> {{ entry.location }}</p>
            <p><strong>Total:</strong> {{ total(entry) }}</p>
          </div>
        </LPopup>
      </LCircleMarker>
    </LMap>
  </div>
</template>

<style>
.l-map {
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
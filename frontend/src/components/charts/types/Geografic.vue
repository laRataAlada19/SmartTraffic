<script setup>
import { ref, computed, onMounted } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  Filler, 
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const geoJson = ref(null);
const geoReady = ref(false);

onMounted(async () => {
  const res = await fetch('https://public.opendatasoft.com/explore/dataset/georef-portugal-distrito/download/?format=geojson');
  const topoJson = await res.json();

  geoJson.value = {
    ...topoJson,
    features: topoJson.features.map(f => ({
      type: f.type,
      properties: { ...f.properties },
      geometry: JSON.parse(JSON.stringify(f.geometry)),
    })),
  };

  geoReady.value = true;
  console.log('Features carregadas:', geoJson.value.features.length);
});

const chartData = computed(() => {
  if (!geoJson.value) return { labels: [], datasets: [] };

  const valueMap = props.data.reduce((acc, curr) => {
    acc[curr.district] = curr.value;
    return acc;
  }, {});

  const featuresWithValue = geoJson.value.features.map(feature => {
    const districtName = feature.properties.NOME;
    return {
      ...feature,
      value: valueMap[districtName] || 0,
    };
  });

  return {
    labels: featuresWithValue.map(f => f.properties.NOME),
    datasets: [
      {
        label: 'Tráfego por Distrito',
        data: featuresWithValue.map(f => f.value),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  };
});
</script>

<template>
  <div v-if="geoReady">
    <h3>Mapa Geográfico</h3>
    <Bar :data="chartData" :options="{ responsive: true }" />
  </div>
  <div v-else>
    <p>Carregando dados geográficos...</p>
  </div>
</template>

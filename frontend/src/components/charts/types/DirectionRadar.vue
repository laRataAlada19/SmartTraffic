<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/DirectionRadar.vue
import { computed } from 'vue';
import { Radar } from 'vue-chartjs';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend ,
  } from 'chart.js';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

// Accept the preloaded data as a prop
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];

const totalByDir = computed(() =>
  directions.map(dir =>
    props.data.reduce((sum, d) => sum + (d[dir] || 0), 0)
  )
);
</script>

<template>
  <Radar :data="{
    labels: ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'],
    datasets: [{
      label: 'Direção de tráfego',
      data: totalByDir,
      backgroundColor: 'rgba(255, 206, 86, 0.2)',
      borderColor: 'rgba(255, 206, 86, 1)',
      borderWidth: 2
    }]
  }" :options="{ responsive: true }" />
</template>
<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/ODMatrix.vue
import { computed } from 'vue';

// Accept the preloaded data as a prop
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

// Extract unique locations from the data
const locations = computed(() => {
  return Array.from(new Set(props.data.flatMap(d => [d.location, d.destination])));
});

// Build the origin-destination matrix
const matrix = computed(() => {
  const result = locations.value.reduce((acc, origin) => {
    acc[origin] = {};
    locations.value.forEach(dest => (acc[origin][dest] = 0));
    return acc;
  }, {});

  props.data.forEach(entry => {
    if (entry.location && entry.destination) {
      result[entry.location][entry.destination] +=
        entry.car + entry.motorcycle + entry.bike + entry.truck + entry.bus;
    }
  });

  return result;
});

// Helper function to determine cell color based on value
const getColor = value => {
  const alpha = Math.min(1, value / 50);
  return `rgba(75, 192, 192, ${alpha})`;
};
</script>

<template>
  <div>
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
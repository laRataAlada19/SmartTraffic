<script setup>
// filepath: /Users/franciscocordeiro/Documents/GitHub/projeto_informatico2/frontend/src/components/charts/types/GrowthRate.vue
import { computed } from 'vue';

// Accept the preloaded data as a prop
const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

// Helper function to calculate the total for a specific date
function totalForDate(date) {
  return props.data
    .filter(d => d.full_date === date)
    .reduce((sum, d) => sum + d.car + d.motorcycle + d.bike + d.truck + d.bus, 0);
}

// Define the dates for comparison
const today = '2025-05-21';
const yesterday = '2025-05-20';

// Compute the growth rate
const growth = computed(() => {
  const t1 = totalForDate(today);
  const t2 = totalForDate(yesterday);
  const diff = t1 - t2;
  return t2 === 0 ? 0 : ((diff / t2) * 100).toFixed(2);
});
</script>

<template>
  <div>
    <h3>Crescimento de tráfego de {{ yesterday }} para {{ today }}:</h3>
    <p :style="{ color: growth >= 0 ? 'green' : 'red' }">
      {{ growth }}%
    </p>
  </div>
</template>
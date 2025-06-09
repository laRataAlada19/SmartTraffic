<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFactVehicleStore } from '@/stores/factvehicle'

const store = useFactVehicleStore()
const data = ref([])

onMounted(async () => {
  data.value = await store.fetchData()
    console.log("Growth Rate data fetched:", data.value)
})

function totalForDate(date) {
  return data.value
    .filter(d => d.full_date === date)
    .reduce((sum, d) => sum + d.car + d.motorcycle + d.bike + d.truck + d.bus, 0)
}

const today = '2025-05-21'
const yesterday = '2025-05-20'

const growth = computed(() => {
  const t1 = totalForDate(today)
  const t2 = totalForDate(yesterday)
  const diff = t1 - t2
  return t2 === 0 ? 0 : ((diff / t2) * 100).toFixed(2)
})
</script>

<template>
  <div>
    <h3>Crescimento de tráfego de {{ yesterday }} para {{ today }}:</h3>
    <p :style="{ color: growth >= 0 ? 'green' : 'red' }">
      {{ growth }}%
    </p>
  </div>
</template>

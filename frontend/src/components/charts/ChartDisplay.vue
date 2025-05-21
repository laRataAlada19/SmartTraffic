<script setup>
import { defineAsyncComponent, computed } from 'vue'
import charts from './chartsConfig'
import { toRefs } from 'vue'
import { BarChart } from 'lucide-vue-next'

const props = defineProps({
  selectedCharts: Array
})

const componentsMap = {
  LineChart: defineAsyncComponent(() => import('./types/LineChart.vue')),
  BarChart: defineAsyncComponent(() => import('./types/Barchart.vue')),
  PieChart: defineAsyncComponent(() => import('./types/PieChart.vue'))
}

const validCharts = computed(() => {
  return (props.selectedCharts || []).map(chartName => ({
    name: chartName,
    component: componentsMap[chartName]
  }))
})

</script>

<template>
  <div>
    <h2>Gráficos Selecionados</h2>
    <div v-for="chart in validCharts" :key="chart.name">
      <component :is="chart.component" />
    </div>
  </div>
</template>

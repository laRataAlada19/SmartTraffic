<script setup>
import { defineAsyncComponent, computed } from 'vue'
import charts from './chartsConfig'
import { toRefs } from 'vue'
import { BarChart } from 'lucide-vue-next'
import Direction from './types/Direction.vue'
import HeatMap from './types/HeatMap.vue'
import Geografic from './types/Geografic.vue'
import Trend from './types/Trend.vue'
import DirectionRadar from './types/DirectionRadar.vue'
import Anomalies from './types/Anomalies.vue'
import ODMatrix from './types/ODMatrix.vue'
import TimeMap from './types/TimeMap.vue'

const props = defineProps({
  selectedCharts: Array
})

const componentsMap = {
  LineChart: defineAsyncComponent(() => import('./types/LineChart.vue')),
  BarChart: defineAsyncComponent(() => import('./types/Barchart.vue')),
  PieChart: defineAsyncComponent(() => import('./types/PieChart.vue')),
  TypeVei: defineAsyncComponent(() => import('./types/TypeVei.vue')),
  Direction: defineAsyncComponent(() => import('./types/Direction.vue')),
  HeatMap: defineAsyncComponent(() => import('./types/HeatMap.vue')),
  Geografic: defineAsyncComponent(() => import('./types/Geografic.vue')),
  HourPic: defineAsyncComponent(() => import('./types/HourPic.vue')),
  ComparePeriods: defineAsyncComponent(() => import('./types/ComparePeriods.vue')),
  GrowthRate : defineAsyncComponent(() => import('./types/GrowthRate.vue')),
  TrafficDensity: defineAsyncComponent(() => import('./types/TrafficDensity.vue')),
  Trend: defineAsyncComponent(() => import('./types/Trend.vue')),
  DirectionRadar: defineAsyncComponent(() => import('./types/DirectionRadar.vue')),
  Anomalies: defineAsyncComponent(() => import('./types/Anomalies.vue')),
  ODMatrix  : defineAsyncComponent(() => import('./types/ODMatrix.vue')),
  TimeMap: defineAsyncComponent(() => import('./types/TimeMap.vue'))
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

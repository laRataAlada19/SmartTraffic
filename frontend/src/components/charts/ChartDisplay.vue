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
async function exportChartData(chartName) {
  const chartData = {
    LineChart: 'line_chart_data.csv',
    BarChart: 'bar_chart_data.csv',
    PieChart: 'pie_chart_data.csv',
    TypeVei: 'type_vei_data.csv',
    Direction: 'direction_data.csv',
    HeatMap: 'heat_map_data.csv',
    Geografic: 'geografic_data.csv',
    HourPic: 'hour_pic_data.csv',
    ComparePeriods: 'compare_periods_data.csv',
    GrowthRate: 'growth_rate_data.csv',
    TrafficDensity: 'traffic_density_data.csv',
    Trend: 'trend_data.csv',
    DirectionRadar: 'direction_radar_data.csv',
    Anomalies: 'anomalies_data.csv',
    ODMatrix: 'od_matrix_data.csv',
    TimeMap: 'time_map_data.csv'
  };

  const fileName = chartData[chartName];
  if (!fileName) {
    console.error(`Não há dados para exportar do gráfico: ${chartName}`);
    return;
  }

  try {
    const response = await fetch(`/api/export/${fileName}`);
    if (!response.ok) throw new Error(`Erro ao exportar dados (${response.status})`);

    const blob = await response.blob();
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    console.log(`Exportado: ${fileName}`);
  } catch (err) {
    console.error('Erro ao exportar gráfico:', err);
  }
}


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
    <div v-for="chart in selectedCharts" :key="chart">
      <component :is="componentsMap[chart]" />
      <button @click="exportChartData(chart)" style="margin-top: 10px;">
        Exportar como CSV
      </button>
    </div>
  </div>
</template>

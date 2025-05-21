<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import charts from './chartsConfig'
import { defineAsyncComponent } from 'vue'

const selectedCharts = ref([])
const router = useRouter()

const componentsMap = {
  LineChart: defineAsyncComponent(() => import('./types/LineChart.vue')),
  BarChart: defineAsyncComponent(() => import('./types/Barchart.vue')),
  PieChart: defineAsyncComponent(() => import('./types/PieChart.vue'))
}

function toggle(chartComponentName) {
  if (selectedCharts.value.includes(chartComponentName)) {
    selectedCharts.value = selectedCharts.value.filter(c => c !== chartComponentName)
  } else {
    selectedCharts.value.push(chartComponentName)
  }
}

function confirmarSelecao() {
  router.push({
    name: 'main',
    query: {
      charts: selectedCharts.value.join(',')
    }
  })
}
</script>

<template>
  <div>
    <h1>Selecionar Gráficos</h1>

    <div
      v-for="chart in charts"
      :key="chart.component"
      class="chart-box"
      style="border: 1px solid #ccc; margin: 1rem 0; padding: 1rem; border-radius: 10px;"
    >
      <label>
        <input
          type="checkbox"
          :checked="selectedCharts.includes(chart.component)"
          @change="toggle(chart.component)"
        />
        {{ chart.name }}
      </label>

      <!-- Componente do gráfico sempre visível -->
      <component :is="componentsMap[chart.component]" />
      
    </div>

    <button @click="confirmarSelecao" style="margin-top: 20px;">Confirmar Seleção</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import charts from './chartsConfig'
import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '@/stores/auth';

const selectedCharts = ref([])
const router = useRouter()
const storeAuth = useAuthStore()

const componentsMap = {
  LineChart: defineAsyncComponent(() => import('./types/LineChart.vue')),
  BarChart: defineAsyncComponent(() => import('./types/Barchart.vue')),
  PieChart: defineAsyncComponent(() => import('./types/PieChart.vue')),
  TypeVei: defineAsyncComponent(() => import('./types/TypeVei.vue')),
  Direction: defineAsyncComponent(() => import('./types/Direction.vue')),
  HeatMap: defineAsyncComponent(() => import('./types/HeatMap.vue')),
  Geografic: defineAsyncComponent(() => import('./types/Geografic.vue')),
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
  <div v-if="!storeAuth.user" class="dashboard-wrapper">
    <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
    <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
  </div>
  <div v-else class="dashboard-wrapper">
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

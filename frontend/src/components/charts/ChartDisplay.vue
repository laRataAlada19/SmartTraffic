<script setup>
import { defineAsyncComponent, ref, onMounted, computed } from 'vue'
import { useFactVehicleStore } from '@/stores/factvehicle'
import charts from './chartsConfig'

const props = defineProps({
  selectedCharts: {
    type: Array,
    required: true,
    default: () => []
  }
})

// Configuração dos componentes dinâmicos
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
  GrowthRate: defineAsyncComponent(() => import('./types/GrowthRate.vue')),
  TrafficDensity: defineAsyncComponent(() => import('./types/TrafficDensity.vue')),
  Trend: defineAsyncComponent(() => import('./types/Trend.vue')),
  DirectionRadar: defineAsyncComponent(() => import('./types/DirectionRadar.vue')),
  Anomalies: defineAsyncComponent(() => import('./types/Anomalies.vue')),
  ODMatrix: defineAsyncComponent(() => import('./types/ODMatrix.vue')),
  TimeMap: defineAsyncComponent(() => import('./types/TimeMap.vue'))
}

// Gerenciamento de dados
const store = useFactVehicleStore()
const sharedData = ref([])
const isDataLoaded = ref(false)
const loadingError = ref(null)

// Busca os dados
const fetchData = async () => {
  try {
    if (!isDataLoaded.value) {
      sharedData.value = await store.fetchData()
      isDataLoaded.value = true
      console.log('Dados carregados:', sharedData.value)
    }
  } catch (error) {
    console.error('Erro ao carregar dados:', error)
    loadingError.value = 'Erro ao carregar dados. Tente recarregar a página.'
    isDataLoaded.value = false
  }
}

// Filtra apenas os gráficos selecionados que existem na configuração
const validCharts = computed(() => {
  return props.selectedCharts
    .filter(chartName => componentsMap[chartName])
    .map(chartName => ({
      name: chartName,
      component: componentsMap[chartName],
      config: charts.find(c => c.component === chartName)
    }))
})

// Função para exportar dados
async function exportChartData(chartName) {
  try {
    const chartConfig = charts.find(c => c.component === chartName)
    if (!chartConfig) {
      console.error(`Configuração não encontrada para o gráfico: ${chartName}`)
      return
    }

    // Simula a exportação - implemente a lógica real conforme sua API
    const fileName = `${chartName.toLowerCase()}_data.csv`
    const dataToExport = sharedData.value
    
    // Cria um CSV simples (substitua pela sua lógica real)
    let csvContent = "data:text/csv;charset=utf-8,"
    
    if (dataToExport.length > 0) {
      // Cabeçalhos
      const headers = Object.keys(dataToExport[0])
      csvContent += headers.join(",") + "\r\n"
      
      // Dados
      dataToExport.forEach(item => {
        csvContent += headers.map(header => item[header]).join(",") + "\r\n"
      })
    }

    const encodedUri = encodeURI(csvContent)
    const link = document.createElement("a")
    link.setAttribute("href", encodedUri)
    link.setAttribute("download", fileName)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    console.log(`Dados exportados: ${fileName}`)
  } catch (err) {
    console.error('Erro ao exportar dados:', err)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="selected-charts-container">
    <!-- Mensagem de carregamento ou erro -->
    <div v-if="!isDataLoaded && !loadingError" class="loading-message">
      <div class="spinner"></div>
      <p>Carregando dados...</p>
    </div>
    
    <div v-if="loadingError" class="error-message">
      {{ loadingError }}
      <button @click="fetchData" class="retry-button">Tentar novamente</button>
    </div>

    <!-- Gráficos selecionados -->
    <div v-if="isDataLoaded" class="charts-grid">
      <div v-for="chart in validCharts" :key="chart.name" class="chart-wrapper">
        <div class="chart-header">
          <h3>{{ chart.config?.name || chart.name }}</h3>
          <button 
            @click="exportChartData(chart.name)" 
            class="export-button"
            title="Exportar dados"
          >
            Exportar
          </button>
        </div>
        <div class="chart-container">
          <component 
            :is="chart.component" 
            :data="sharedData"
            v-if="isDataLoaded"
          />
        </div>
        <p class="chart-description" v-if="chart.config?.description">
          {{ chart.config.description }}
        </p>
      </div>
    </div>

    <div v-if="isDataLoaded && validCharts.length === 0" class="no-charts-message">
      Nenhum gráfico válido selecionado. Por favor, selecione gráficos na página de configuração.
    </div>
  </div>
</template>

<style scoped>
.selected-charts-container {
  padding: 1rem;
  width: 100%;
}

.loading-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  padding: 1rem;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  text-align: center;
  margin-bottom: 1rem;
}

.retry-button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #c62828;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.chart-wrapper {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.export-button {
  padding: 0.25rem 0.5rem;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.export-button:hover {
  background-color: #e0e0e0;
}

.chart-container {
  min-height: 300px;
}

.chart-description {
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #666;
  font-style: italic;
}

.no-charts-message {
  padding: 2rem;
  text-align: center;
  color: #666;
  background-color: #f5f5f5;
  border-radius: 8px;
}
</style>
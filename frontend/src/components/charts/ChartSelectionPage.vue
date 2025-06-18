<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import charts from './chartsConfig';
import { defineAsyncComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useFactVehicleStore } from '@/stores/factvehicle';

const groupedCharts = computed(() => {
  const groups = {};
  charts.forEach(chart => {
    const type = chart.type || 'outros';
    if (!groups[type]) groups[type] = [];
    groups[type].push(chart);
  });
  return groups;
});

const allData = ref([]);
const selectedDestinations = ref({});
const selectedCharts = computed(() => Object.keys(selectedDestinations.value));
const router = useRouter();
const storeAuth = useAuthStore();

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
};

function toggle(chartComponentName, destination) {
  const current = selectedDestinations.value[chartComponentName] || [];

  if (current.includes(destination)) {
    selectedDestinations.value[chartComponentName] = current.filter(d => d !== destination);
  } else {
    selectedDestinations.value[chartComponentName] = [...current, destination];
  }
}

async function confirmarSelecao() {
  try {
    const dashboardCharts = [];
    const locationCharts = [];

    for (const [chart, destinations] of Object.entries(selectedDestinations.value)) {
      if (destinations.includes('Dashboard')) {
        dashboardCharts.push(chart);
      }
      if (destinations.includes('Location')) {
        locationCharts.push(chart);
      }
    }

    const parts = [];
    if (dashboardCharts.length > 0) {
      parts.push(`Dashboard:${dashboardCharts.join(',')}`);
    }
    if (locationCharts.length > 0) {
      parts.push(`Location:${locationCharts.join(',')}`);
    }

    const formattedTable = parts.join(';');
    console.log('Gráficos selecionados:', formattedTable);
    await storeAuth.addTable(formattedTable);

    router.push({
      name: 'main',
      query: {
        charts: [...new Set([...dashboardCharts, ...locationCharts])].join(','),
      },
    });
  } catch (error) {
    console.error('Erro ao guardar os gráficos selecionados:', error);
  }
}

const store = useFactVehicleStore();
const sharedData = ref([]);
const isDataLoaded = ref(false);

// opcional: computed com toRaw se mesmo assim quiseres dados puros
const rawSharedData = computed(() => sharedData.value);

const fetchData = async () => {
  if (!isDataLoaded.value) {
    try {
      const data = await store.fetchData();
      sharedData.value = data || [];
      isDataLoaded.value = true;
      console.log('Dados carregados:', sharedData.value);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      sharedData.value = [];
      isDataLoaded.value = true;
    }
  }
};

onMounted(async () => {
  await fetchData();

  try {
    const tables = await storeAuth.getTables();
    console.log('Tabelas do user:', tables);

    if (tables.tables) {
      const dashboardCharts = tables.tables.Dashboard || [];
      const locationCharts = tables.tables.Location || [];
      const combinedCharts = new Set([...dashboardCharts, ...locationCharts]);

      combinedCharts.forEach(chart => {
        const destinations = [];
        if (dashboardCharts.includes(chart)) destinations.push('Dashboard');
        if (locationCharts.includes(chart)) destinations.push('Location');
        selectedDestinations.value[chart] = destinations;
      });
    }
  } catch (error) {
    console.error('Erro ao buscar tabelas do user:', error);
  }
});
</script>

<template>
  <div v-if="!storeAuth.user" class="dashboard-wrapper">
    <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
    <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
  </div>

  <div v-else class="dashboard-wrapper">
    <h1 class="dashboard-title">Selecionar Gráficos:</h1>

    <div class="chart-group" v-for="(charts, type) in groupedCharts" :key="type">
      <h2 class="chart-type-title">{{ type.toUpperCase() }}</h2>
      <div class="chart-grid">
        <div v-for="chart in charts" :key="chart.component" class="chart-box">
          <div class="destination-options">
            <h3 class="destination-title">Destino do Gráfico:</h3>
            <label>
              <input type="checkbox" :checked="selectedDestinations[chart.component]?.includes('Dashboard')"
                @change="toggle(chart.component, 'Dashboard')" />
              Dashboard
            </label>
            <label>
              <input type="checkbox" :checked="selectedDestinations[chart.component]?.includes('Location')"
                @change="toggle(chart.component, 'Location')" />
              Localização
            </label>
          </div>
          <strong>{{ chart.name }}</strong>
          <p class="chart-description">{{ chart.description }}</p>

          <component 
            v-if="isDataLoaded" 
            :is="componentsMap[chart.component]" 
            :data="rawSharedData"
            @mounted="console.log('Component mounted:', chart.component, 'with data:', rawSharedData)"
          />
        </div>
      </div>
    </div>

    <button class="btn-confirm" @click="confirmarSelecao">Confirmar Seleção</button>

    <h3>Gráficos Selecionados:</h3>

    <div v-if="!isDataLoaded" style="text-align: center; margin-top: 30px;">
      <span class="spinner"></span>
      <p>Carregando dados...</p>
    </div>

    <div v-else>
      <div v-for="chart in selectedCharts" :key="chart">
        <component
          v-if="isDataLoaded"
          :is="componentsMap[chart]"
          :data="rawSharedData"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-group {
  margin-bottom: 2rem;
}

.chart-group h2 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #ccc;
}

.dashboard-wrapper {
  padding: 2rem;
  max-width: 100%;
  margin: 0 auto;
}

.dashboard-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.chart-box {
  border: 1px solid #ccc;
  padding: 0.75rem;
  border: none;
  background-color: #1C2541;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.chart-box:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chart-description {
  font-size: 0.9rem;
  color: #ccc;
  font-style: italic;
  margin-top: 0.5rem;
}

.destination-options {
  margin-bottom: 0.75rem;
}

.destination-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.destination-options label {
  margin-right: 20px;
  font-size: 0.95rem;
}

.btn-confirm {
  background-color: #4CAF50;
  color: white;
  padding: 10px 16px;
  margin-top: 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-confirm:hover {
  background-color: #45a049;
}

/* Spinner simples */
.spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 123, 255, 0.2);
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

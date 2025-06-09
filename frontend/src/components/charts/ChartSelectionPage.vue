<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import charts from './chartsConfig';
import { defineAsyncComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';
import HourPic from './types/HourPic.vue';
import ComparePeriods from './types/ComparePeriods.vue';
import GrowthRate from './types/GrowthRate.vue';
import TrafficDensity from './types/TrafficDensity.vue';


const selectedDestinations = ref({});
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
  GrowthRate : defineAsyncComponent(() => import('./types/GrowthRate.vue')),
  TrafficDensity: defineAsyncComponent(() => import('./types/TrafficDensity.vue')),
  Trend: defineAsyncComponent(() => import('./types/Trend.vue')),
  DirectionRadar: defineAsyncComponent(() => import('./types/DirectionRadar.vue')),
  Anomalies: defineAsyncComponent(() => import('./types/Anomalies.vue')),
  ODMatrix  : defineAsyncComponent(() => import('./types/ODMatrix.vue')),
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

onMounted(() => {
  storeAuth.getTables().then((tables) => {

    console.log('Tabelas do user:', tables);

    console.log('Tabelas do user data:', tables.tables.Dashboard);

    if (tables.tables) {
      const dashboardCharts = tables.tables.Dashboard;
      const locationCharts = tables.tables.Location;
      if (dashboardCharts) {
        dashboardCharts.forEach((chart) => {
          dashboardCharts.push(chart);
        });
      }
      console.log('Dashboard Charts:', dashboardCharts);
      console.log('Location Charts:', locationCharts);
      if (locationCharts) {
        locationCharts.forEach((chart) => {
          locationCharts.push(chart);
        });
      }

      if(dashboardCharts && locationCharts){
      const combinedCharts = new Set([...dashboardCharts, ...locationCharts]);
      combinedCharts.forEach(chart => {
        const destinations = [];
        if (dashboardCharts.includes(chart)) destinations.push('Dashboard');
        if (locationCharts.includes(chart)) destinations.push('Location');
        selectedDestinations.value[chart] = destinations;
      });
      }else if(dashboardCharts){
        const combinedCharts = new Set([...dashboardCharts,]);
        combinedCharts.forEach(chart => {
        const destinations = [];
        if (dashboardCharts.includes(chart)) destinations.push('Dashboard');
        selectedDestinations.value[chart] = destinations;
      });
    }
    } else if (locationCharts) {
      const combinedCharts = new Set([...locationCharts]);
      combinedCharts.forEach(chart => {
        const destinations = [];
        if (locationCharts.includes(chart)) destinations.push('Location');
        selectedDestinations.value[chart] = destinations;
      });
    } else {
      console.warn('Nenhuma tabela encontrada para o user.');
    }
  }).catch((error) => {
    console.error('Erro ao buscar tabelas do user:', error);
  });
});
</script>


<template>
  <div v-if="!storeAuth.user" class="dashboard-wrapper">
    <h1 style="text-align: center; margin-top: 20px;">Aceda ao dashboard</h1>
    <p style="text-align: center; margin-bottom: 20px;">Por favor, faça login para aceder ao dashboard.</p>
  </div>
  <div v-else class="dashboard-wrapper">
    <h1 class="dashboard-title">Selecionar Gráficos:</h1>

    <div class="chart-grid">
      <div v-for="chart in charts" :key="chart.component" class="chart-box">
        <div class="destination-options">
          <h2 class="destination-title">Destino do Gráfico:</h2>
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
        <component :is="componentsMap[chart.component]" />
      </div>
    </div>

    <button class="btn-confirm" @click="confirmarSelecao">Confirmar Seleção</button>
  </div>
</template>


<style scoped>
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
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}
.chart-box:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.chart-description {
  font-size: 0.9rem;
  color: #555;
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
</style>
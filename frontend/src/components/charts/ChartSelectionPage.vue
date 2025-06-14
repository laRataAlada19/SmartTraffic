<script setup>
import { onMounted, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import charts from './chartsConfig';
import { defineAsyncComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { toast } from '@/components/ui/toast';
import HourPic from './types/HourPic.vue';
import ComparePeriods from './types/ComparePeriods.vue';
import GrowthRate from './types/GrowthRate.vue';
import TrafficDensity from './types/TrafficDensity.vue';

const groupedCharts = computed(() => {
  const groups = {};
  charts.forEach(chart => {
    const type = chart.type || 'outros';
    if (!groups[type]) groups[type] = [];
    groups[type].push(chart);
  });
  return groups;
});

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
    await storeAuth.addTable(formattedTable);

    router.push({
      name: 'main',
      query: {
        charts: [...new Set([...dashboardCharts, ...locationCharts])].join(','),
      },
    });
  } catch (error) {
    console.error('Erro ao guardar os gráficos selecionados:', error);
    toast({
      title: 'Erro',
      description: 'Ocorreu um erro ao guardar os gráficos selecionados.',
    });
  }
}

onMounted(() => {
  storeAuth.getTables().then((tables) => {
    if (tables.tables) {
      const dashboardCharts = tables.tables.Dashboard;
      const locationCharts = tables.tables.Location;
      if (dashboardCharts) {
        dashboardCharts.forEach((chart) => {
          dashboardCharts.push(chart);
        });
      }

      if (locationCharts) {
        locationCharts.forEach((chart) => {
          locationCharts.push(chart);
        });
      }

      if (dashboardCharts && locationCharts) {
        const combinedCharts = new Set([...dashboardCharts, ...locationCharts]);
        combinedCharts.forEach(chart => {
          const destinations = [];
          if (dashboardCharts.includes(chart)) destinations.push('Dashboard');
          if (locationCharts.includes(chart)) destinations.push('Location');
          selectedDestinations.value[chart] = destinations;
        });
      } else if (dashboardCharts) {
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
      toast({
        title: 'Aviso',
        description: 'Nenhuma tabela encontrada para o user. Por favor, selecione os gráficos desejados.',
      });
    }
  }).catch((error) => {
    console.error('Erro ao buscar tabelas do user:', error);
    toast({
      title: 'Erro',
      description: 'Ocorreu um erro ao buscar as tabelas do user.',
    });
  });
});
</script>

<template>
  <!--
  <div v-if="!storeAuth.user" class="dashboard-wrapper">
    <h1 class="text-center mt-6">Aceda ao dashboard</h1>
    <p class="text-center mb-6">Por favor, faça login para aceder ao dashboard.</p>
  </div>
  <div v-else class="dashboard-wrapper">
  -->
  <h1 class="dashboard-title">Configuração</h1>

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
        <strong class="chart-name">{{ chart.name }}</strong>
        <p class="chart-description">{{ chart.description }}</p>
        <component :is="componentsMap[chart.component]" />
      </div>
    </div>
  </div>

  <button class="btn-confirm" @click="confirmarSelecao">Confirmar Seleção</button>
  <!--</div>-->
</template>

<style scoped>
.dashboard-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: #5BC0BE;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #5BC0BE;
  padding-bottom: 0.5rem;
}

.chart-group {
  margin-bottom: 2.5rem;
}

.chart-type-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #B0BEC5;
  margin-bottom: 1rem;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.5rem;
}

.chart-box {
  background-color: #1C2541;
  border-radius: 0.75rem;
  padding: 1rem;
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.3s ease;
}

.chart-box:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.destination-options {
  margin-bottom: 1rem;
}

.destination-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #5BC0BE;
}

.destination-options label {
  margin-right: 1.5rem;
  font-size: 0.95rem;
  color: #E0E0E0;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}

.chart-name {
  font-weight: 600;
  font-size: 1rem;
  color: #FAFAFA;
}

.chart-description {
  font-size: 0.875rem;
  font-style: italic;
  color: #B0BEC5;
  margin-top: 0.25rem;
  margin-bottom: 1rem;
}

.btn-confirm {
  background-color: #5BC0BE;
  color: #0B132B;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  margin-top: 2rem;
  transition: background-color 0.3s ease;
}

.btn-confirm:hover {
  background-color: #3A506B;
}
</style>

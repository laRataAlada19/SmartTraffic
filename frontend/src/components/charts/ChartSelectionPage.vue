<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import charts from './chartsConfig';
import { defineAsyncComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';


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

      // Build initial selectedDestinations map
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
    <br><br><br><br>
    <h1>Selecionar Gráficos</h1>

    <div v-for="chart in charts" :key="chart.component" class="chart-box"
      style="border: 1px solid #ccc; margin: 1rem 0; padding: 1rem; border-radius: 10px;">
      <div class="destination-options">
        <h2>Destino do Gráfico</h2>
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
      {{ chart.name }}
      <component :is="componentsMap[chart.component]" />
    </div>

    <button class="btn-confirm" @click="confirmarSelecao">Confirmar Seleção</button>
  </div>
</template>

<style scoped>
.btn-confirm {
  background-color: #4CAF50;
  color: white;
  padding: 6px 12px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
}

.destination-options {
  margin-top: 10px;
  margin-bottom: 10px;
}

.destination-options label {
  margin-right: 20px;
}
</style>
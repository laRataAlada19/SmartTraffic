<script setup>
import { ref, computed } from 'vue';
import dayjs from 'dayjs';

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const locationFilter = ref('Todos');
const timeInterval = ref('dia');
const dateRange = ref({
  start: '',
  end: ''
});
const vehicleTypeFilter = ref('Todos');

const vehicleTypes = [
  { id: 'Todos', label: 'Todos os Veículos' },
  { id: 'car', label: 'Carros' },
  { id: 'motorcycle', label: 'Motociclos' },
  { id: 'bike', label: 'Bicicletas' },
  { id: 'truck', label: 'Camiões' },
  { id: 'bus', label: 'Autocarros' }
];

const locations = computed(() => {
  const uniqueLocations = new Set();
  props.data.forEach(entry => {
    if (entry.location) uniqueLocations.add(entry.location);
    if (entry.destination) uniqueLocations.add(entry.destination);
  });
  return ['Todos', ...Array.from(uniqueLocations).sort()];
});

const filteredData = computed(() => {
  let data = [...props.data];

  if (locationFilter.value !== 'Todos') {
    data = data.filter(d => 
      d.location === locationFilter.value || 
      d.destination === locationFilter.value
    );
  }

  if (timeInterval.value === 'custom' && dateRange.value.start && dateRange.value.end) {
    data = data.filter(d => {
      const date = dayjs(d.full_date);
      return date.isAfter(dayjs(dateRange.value.start).subtract(1, 'day')) && 
             date.isBefore(dayjs(dateRange.value.end).add(1, 'day'));
    });
  } else if (timeInterval.value !== 'custom') {
    const now = dayjs();
    data = data.filter(d => {
      const date = dayjs(d.full_date);
      switch (timeInterval.value) {
        case 'dia': return date.isSame(now, 'day');
        case 'semana': return date.isAfter(now.subtract(1, 'week'));
        case 'mes': return date.isAfter(now.subtract(1, 'month'));
        case 'ano': return date.isAfter(now.subtract(1, 'year'));
        default: return true;
      }
    });
  }

  return data;
});

const matrix = computed(() => {
  const result = {};
  const allLocations = locations.value.filter(loc => loc !== 'Todos');

  allLocations.forEach(origin => {
    result[origin] = {};
    allLocations.forEach(dest => (result[origin][dest] = 0));
  });

  filteredData.value.forEach(entry => {
    if (entry.location && entry.destination) {
      let total = 0;
      
      if (vehicleTypeFilter.value === 'Todos') {
        total = (Number(entry.car) || 0) + (Number(entry.motorcycle) || 0) +
                (Number(entry.bike) || 0) + (Number(entry.truck) || 0) +
                (Number(entry.bus) || 0);
      } else {
        total = Number(entry[vehicleTypeFilter.value]) || 0;
      }

      result[entry.location][entry.destination] += total;
    }
  });
  console.log('Matriz origem-destino:', result);

  return result;
});

const getColor = (value) => {
  if (value === 0) return 'rgba(0,0,0,0)';
  
  const maxValue = Math.max(
    ...Object.values(matrix.value).flatMap(row => 
      Object.values(row)
    ),
    1
  );
  
  const alpha = Math.min(1, value / maxValue * 0.8 + 0.2); 
  return `rgba(75, 192, 192, ${alpha})`; 
};

const displayLocations = computed(() => 
  locations.value.filter(loc => loc !== 'Todos')
);

</script>

<template>
  <div class="matrix-container bg-slate-800 text-white p-4 rounded-xl shadow-lg">
    <div class="filter-container mb-4">
      <div class="filter-group">
        <label class="filter-label">
          Localidade:
          <select v-model="locationFilter" class="filter-select">
            <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
          </select>
        </label>
      </div>

      <div class="filter-group">
        <label class="filter-label">
          Tipo de Veículo:
          <select v-model="vehicleTypeFilter" class="filter-select">
            <option v-for="type in vehicleTypes" :key="type.id" :value="type.id">
              {{ type.label }}
            </option>
          </select>
        </label>
      </div>

      <div class="filter-group">
        <label class="filter-label">
          Período:
          <select v-model="timeInterval" class="filter-select">
            <option value="dia">Hoje</option>
            <option value="semana">Última Semana</option>
            <option value="mes">Último Mês</option>
            <option value="ano">Último Ano</option>
            <option value="custom">Personalizado</option>
          </select>
        </label>
      </div>

      <template v-if="timeInterval === 'custom'">
        <div class="filter-group">
          <label class="filter-label">
            Data Início:
            <input 
              type="date" 
              v-model="dateRange.start" 
              class="filter-select"
            />
          </label>
        </div>
        <div class="filter-group">
          <label class="filter-label">
            Data Fim:
            <input 
              type="date" 
              v-model="dateRange.end" 
              class="filter-select"
            />
          </label>
        </div>
      </template>
    </div>

    <div class="matrix-content">

      <div class="overflow-x-auto">
        <table class="min-w-full border border-slate-600 text-sm">
          <thead class="bg-slate-700 sticky top-0">
            <tr>
              <th class="border border-slate-600 px-3 py-2 text-left">Origem \ Destino</th>
              <th 
                v-for="dest in displayLocations" 
                :key="dest" 
                class="border border-slate-600 px-3 py-2 text-left"
              >
                {{ dest }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="origin in displayLocations" :key="origin">
              <th class="border border-slate-600 px-3 py-2 text-left bg-slate-700 sticky left-0 z-10">
                {{ origin }}
              </th>
              <td
                v-for="dest in displayLocations"
                :key="dest"
                class="border border-slate-600 px-3 py-2 text-center"
                :style="{ backgroundColor: getColor(matrix[origin]?.[dest] || 0) }"
                :title="`${origin} → ${dest}: ${matrix[origin]?.[dest] || 0} veículos`"
              >
                {{ matrix[origin]?.[dest] || 0 }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="text-xs text-slate-400 mt-3">
        <span class="inline-block w-4 h-4 mr-1 rounded" style="background-color: rgba(75, 192, 192, 0.2)"></span> Pouco tráfego
        <span class="inline-block w-4 h-4 mx-1 rounded" style="background-color: rgba(75, 192, 192, 0.5)"></span> Médio
        <span class="inline-block w-4 h-4 mx-1 rounded" style="background-color: rgba(75, 192, 192, 0.8)"></span> Intenso
      </div>
    </div>
  </div>
</template>

<style scoped>
.matrix-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 100%;
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: flex-end;
}

.filter-group {
  flex: 1;
  min-width: 200px;
}

.filter-label {
  font-weight: 500;
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
}

.filter-select {
  margin-top: 0.3rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #475569;
  border-radius: 6px;
  font-size: 0.95rem;
  background-color: #1e293b;
  color: #f8fafc;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.matrix-content {
  background-color: #1e293b;
  border-radius: 8px;
  padding: 1rem;
}

table {
  border-collapse: collapse;
}

th, td {
  padding: 0.5rem 0.75rem;
}

td:hover {
  filter: brightness(1.1);
}
</style>
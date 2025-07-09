<script setup>
import { ref, computed, watch } from 'vue';
import dayjs from 'dayjs';

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => [],
  },
});

const dateRange = ref({
  start: dayjs().subtract(1, 'day').format('YYYY-MM-DD'),
  end: dayjs().format('YYYY-MM-DD')
});
const locationFilter = ref('Todos');

const locations = computed(() => {
  if (!Array.isArray(props.data)) return ['Todos'];
  const unique = new Set(props.data.map(entry => entry.location || 'Desconhecido'));
  return ['Todos', ...unique];
});

const totalForDate = computed(() => (date) => {
  let filteredData = [...props.data];

  if (locationFilter.value !== 'Todos') {
    filteredData = filteredData.filter(d => d.location === locationFilter.value);
  }

  return filteredData
    .filter(d => d.full_date === date)
    .reduce((sum, d) => sum + (d.car || 0) + (d.motorcycle || 0) + (d.bike || 0) + (d.truck || 0) + (d.bus || 0), 0);
});

const growthValue = computed(() => {
  const start = totalForDate.value(dateRange.value.start);
  const end = totalForDate.value(dateRange.value.end);

  if (start === 0 && end === 0) return 0;
  if (start === 0 && end > 0) return Infinity;

  const diff = end - start;
  return (diff / start) * 100;
});

const growthRate = computed(() => {
  if (growthValue.value === Infinity) return 'Novo fluxo';
  return `${growthValue.value.toFixed(2)}%`;
});

const totals = computed(() => ({
  start: totalForDate.value(dateRange.value.start),
  end: totalForDate.value(dateRange.value.end)
}));

const formattedDates = computed(() => ({
  start: dayjs(dateRange.value.start).format('DD/MM/YYYY'),
  end: dayjs(dateRange.value.end).format('DD/MM/YYYY')
}));

const growthStyle = computed(() => ({
  color: growthValue.value > 0 ? '#10B981' : growthValue.value < 0 ? '#EF4444' : '#6b7280',
  fontWeight: 'bold',
  fontSize: '1.2rem'
}));

const growthIcon = computed(() => {
  if (growthValue.value === Infinity) return '↗';
  return growthValue.value >= 0 ? '↑' : '↓';
});
</script>

<template>
  <div class="growth-rate-container">
    <div class="filter-container">
      <label class="filter-label">
        Localidade:
        <select v-model="locationFilter" class="filter-select">
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </label>

      <label class="filter-label">
        Data Inicial:
        <input 
          type="date" 
          v-model="dateRange.start" 
          :max="dateRange.end" 
          class="filter-select"
        />
      </label>

      <label class="filter-label">
        Data Final:
        <input 
          type="date" 
          v-model="dateRange.end" 
          :min="dateRange.start" 
          class="filter-select"
        />
      </label>
    </div>

    <div class="indicator-card">
      <div class="indicator-header">
        <h3>Taxa de Crescimento do Tráfego</h3>
        <p class="date-range">{{ formattedDates.start }} - {{ formattedDates.end }}</p>
      </div>

      <div class="indicator-body">
        <div class="growth-display">
          <span :style="growthStyle">{{ growthIcon }} {{ growthRate }}</span>
        </div>

        <div class="absolute-values">
          <div class="value-box">
            <span class="value-label">Total em {{ formattedDates.start }}</span>
            <span class="value-number">{{ totals.start }}</span>
          </div>
          <div class="value-box">
            <span class="value-label">Total em {{ formattedDates.end }}</span>
            <span class="value-number">{{ totals.end }}</span>
          </div>
        </div>
      </div>

      <div class="indicator-footer">
        <p v-if="growthValue === Infinity" class="positive-message">
          Fluxo iniciado após ausência total de tráfego
        </p>
        <p v-else-if="growthValue > 0" class="positive-message">
          Aumento no fluxo de veículos no período
        </p>
        <p v-else-if="growthValue < 0" class="negative-message">
          Redução no fluxo de veículos no período
        </p>
        <p v-else class="neutral-message">
          Estabilidade no fluxo de veículos
        </p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.growth-rate-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 800px;
  margin: 0 auto;
}

.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  align-items: flex-end;
}

.filter-label {
  font-weight: 500;
  color: #fff;
  display: flex;
  flex-direction: column;
  font-size: 0.95rem;
  min-width: 180px;
}

.filter-select {
  margin-top: 0.3rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: #fff;
  color: #333;
  transition: border-color 0.2s;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.indicator-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  border-left: 4px solid #3b82f6;
}

.indicator-header {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.75rem;
}

.indicator-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.date-range {
  margin: 0.25rem 0 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.indicator-body {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.growth-display {
  text-align: center;
  margin: 1rem 0;
}

.growth-display span {
  font-size: 2.5rem;
  display: inline-block;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  background-color: #f9fafb;
}

.absolute-values {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
}

.value-box {
  flex: 1;
  text-align: center;
  padding: 1rem;
  background-color: #f3f4f6;
  border-radius: 8px;
}

.value-label {
  display: block;
  color: #4b5563;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.value-number {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
}

.indicator-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
  text-align: center;
  font-weight: 500;
}

.positive-message {
  color: #10B981;
}

.negative-message {
  color: #EF4444;
}

.neutral-message {
  color: #6b7280;
}
</style>
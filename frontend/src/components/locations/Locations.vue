<script setup>
// Importações necessárias
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';
import LocationsList from './LocationList.vue';
import LocationCreate from './LocationCreate.vue';

const locationName = ref('');
const direction = ref('');
const locationStore = useLocationStore();
const granularity = ref(1); //default diario

const changeGranularity = (selectedGranularity) => {
    granularity.value = selectedGranularity;
};

onMounted(async () => {
  locationStore.fetchLocations();
});
</script>

<template>
    <br/>
    <br/>
    <br/>
    <br/>

    <div v-if="locationStore.totalLocations > 0" class="flex flex-col items-center">
        <LocationsList :locations="locationStore.locations" />
    </div>
    <div v-else class="flex flex-col items-center">
        <h1 class="text-2xl font-bold mb-4">Nenhuma localização encontrada</h1>
    </div>

    <br/>
    <br/>
    <br/>
    <br/>

    <LocationCreate />
</template>
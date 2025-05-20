<script setup>
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';
import LocationList from '@/components/locations/LocationList.vue';
import LocationCreate from '@/components/locations/LocationCreate.vue';

const locationName = ref('');
const direction = ref('');
const locationStore = useLocationStore();
const granularity = ref(1); //default diário

const changeGranularity = (selectedGranularity) => {
    granularity.value = selectedGranularity;
};

onMounted(async () => {
    await locationStore.fetchLocations();
});
</script>

<template>
    <br>
    <br>
    <br>
    <br>

    <div v-if="locationStore.totalLocations > 0">
        <LocationList :locations="locationStore.locations"></LocationList>
    </div>
    <div v-else>
        <p class="text-center">Nenhum local encontrado.</p>
    </div>

    <br>
    <br>
    <br>
    <br>

    <LocationCreate></LocationCreate>
</template>
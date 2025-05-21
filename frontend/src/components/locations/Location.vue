<script setup>
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';

const locationStore = useLocationStore();
const props = defineProps({
    id: Number
});
const locationId = ref(props.id);
const locationDetails = ref(null);
const granularity = ref(3); //default diario
const startDate = ref('2025-05-01');
const endDate = ref('2025-05-08');

const changeGranularity = (selectedGranularity) => {
    granularity.value = selectedGranularity;
};

onMounted(async () => {
    try {
        locationDetails.value = await locationStore.fetchLocationById(locationId.value);
    } catch (error) {
        console.error('Error fetching location details:', error);
    }
});
</script>

<template>
    <br>
    <br>
    <br>
    <br>

    <div v-if="locationDetails" class="bg-white rounded-lg shadow p-4">
        <header>
            <h2>Informação da Localização</h2>
            <p><strong>Localização:</strong> {{ locationDetails.location }}</p>
            <p><strong>Coordenadas geográficas:</strong></p>
            <p class="latitude">Latitude: </p>
            <p class="longitude">Longitude: </p>
            <p><strong>Direção da câmara:</strong> {{ locationDetails.direction }}</p>
            <div class="btn-actions">
                <button class="btn-edit">Editar</button>
                <button class="btn-delete">Eliminar</button>
            </div>
        </header>

        <section class="statistics">
            <h2>Estatísticas</h2>
            <p><strong>Granularidade temporal</strong></p>
            <div class="controls">
                <label>De:</label>
                <input type="date" v-model="startDate" />
                <label>Até:</label>
                <input type="date" v-model="endDate" />
            </div>

            <div class="granularity-options">
                <label>
                    <input type="radio" value="1" v-model="granularity" @change="changeGranularity(1)" />
                    Por mês
                </label>
                <label>
                    <input type="radio" value="2" v-model="granularity" @change="changeGranularity(2)" />
                    Por semana
                </label>
                <label>
                    <input type="radio" value="3" v-model="granularity" @change="changeGranularity(3)" />
                    Por dia
                </label>
                <label>
                    <input type="radio" value="4" v-model="granularity" @change="changeGranularity(4)" />
                    Por hora
                </label>
            </div>
        </section>
    </div>
</template>

<style scoped>
header {
    max-width: 900px;
    margin: auto;
    background: #f5f5f5;
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 20px;
}

header h2 {
    font-size: 24px;
    text-align: center;
}

header .latitude,
.longitude {
    font-size: 18px;
    margin-left: 57px;
}

.btn-actions {
    margin-top: 10px;
    margin-left: 400px;
}

.btn-edit {
    background-color: #4CAF50;
    color: white;
    padding: 6px 12px;
    margin-right: 10px;
    border: none;
    border-radius: 4px;
}

.btn-delete {
    background-color: #f44336;
    color: white;
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
}

.statistics {
    max-width: 900px;
    margin: auto;
    background: #f5f5f5;
    padding: 30px;
    border-radius: 10px;
}

.statistics h2 {
    font-size: 24px;
    text-align: center;
}

.controls {
    margin-top: 10px;
    margin-left: 30px;
}

.controls input {
    margin-right: 10px;
    padding: 5px;
}

.granularity-options {
    margin-top: 10px;
    margin-left: 30px;
}

.granularity-options label {
    margin-right: 20px;
}
</style>
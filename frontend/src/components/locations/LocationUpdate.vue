<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';
import { useRouter } from 'vue-router';

const locationStore = useLocationStore();
const props = defineProps({
    location: Object
});
const emit = defineEmits(['cancelUpdate']);
const showUpdateForm = ref(true);
const router = useRouter();

let updatedLocation = reactive({
    location: props.location.location,
    direction: props.location.direction,
    latitude: props.location.latitude,
    longitude: props.location.longitude
});

const directions = reactive([
  { name: 'Norte', id: '1' },
  { name: 'Sul', id: '2' },
  { name: 'Este', id: '3' },
  { name: 'Oeste', id: '4' },
  { name: 'Noroeste', id: '5' },
  { name: 'Sudeste', id: '6' },
]);

function updateLocation(location) {
    locationStore.updateLocation(props.location.location_id, location)
    .then(() => {
        alert('Localização atualizada com sucesso!');
        cancelUpdate();//voltar atras
    })
    .catch(error => {
        console.error('Erro ao atualizar localização:', error);
        alert('Ocorreu um erro ao atualizar a localização. Tente novamente.');
    });
}

function cancelUpdate() {
    emit('cancelUpdate', !showUpdateForm.value);
}
</script>

<template>
    <header>
        <h2>Informação da Localização</h2>
        <p><strong>Localização:</strong> <input v-model="updatedLocation.location"/></p>
        <p><strong>Coordenadas geográficas:</strong></p>
        <p class="latitude">Latitude: <input v-model="updatedLocation.latitude"/></p>
        <p class="longitude">Longitude: <input v-model="updatedLocation.longitude"/></p>
        <div>
                <label class="block mb-1">Direção:</label>
                <select v-model="updatedLocation.direction" class="w-full border rounded px-3 py-2">
                    <option disabled value="">Selecione a direção</option>
                    <option v-for="direction in directions" :key="direction.id" :value="direction.name">
                        {{ direction.name }}
                    </option>
                </select>
            </div>
        <div class="btn-actions">
            <button class="btn-edit" @click="updateLocation(updatedLocation)">Guardar</button>
            <button class="btn-delete" @click="cancelUpdate()">Cancelar</button>
        </div>
    </header>
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

.latitude {
    margin-bottom: 10px;
}

header .longitude {
    margin-bottom: 10px;
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
</style>
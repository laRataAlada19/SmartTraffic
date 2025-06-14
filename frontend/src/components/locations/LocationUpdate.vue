<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';
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
            toast({
                title: 'Sucesso',
                description: `Localização ${location.location} atualizada com sucesso!`,
            });
            cancelUpdate();//voltar atras
        })
        .catch(error => {
            console.error('Erro ao atualizar localização:', error);
            toast({
                title: 'Erro',
                description: 'Ocorreu um erro ao atualizar a localização. Tente novamente.',
                variant: 'destructive',
            });
        });
}

function cancelUpdate() {
    emit('cancelUpdate', !showUpdateForm.value);
}
</script>

<template>
    <h1 class="dashboard-title">Atualizar Localização</h1>
    <section class="location-update-card">
        <div class="field-group">
            <label for="location">Localização:</label>
            <input id="location" v-model="updatedLocation.location" />
        </div>

        <div class="field-group">
            <label>Latitude:</label>
            <input v-model="updatedLocation.latitude" />
        </div>

        <div class="field-group">
            <label>Longitude:</label>
            <input v-model="updatedLocation.longitude" />
        </div>

        <div class="field-group">
            <label>Direção:</label>
            <select v-model="updatedLocation.direction">
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
    </section>
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

.location-update-card {
    background-color: #1C2541;
    color: #ffffff;
    padding: 2rem;
    border-radius: 12px;
    max-width: 800px;
    margin: 2rem auto;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.location-update-card h2 {
    font-size: 1.5rem;
    color: #5BC0BE;
    text-align: center;
    margin-bottom: 1.5rem;
}

.field-group {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}

.field-group label {
    font-size: 0.95rem;
    color: #B0BEC5;
    margin-bottom: 0.5rem;
}

.field-group input,
.field-group select {
    padding: 10px;
    border-radius: 6px;
    background-color: #0B132B;
    color: white;
    border: 1px solid #5BC0BE;
    font-size: 1rem;
}

.field-group select {
    appearance: none;
}

.btn-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 2rem;
    gap: 1rem;
}

.btn-edit {
    background-color: #4CAF50;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-edit:hover {
    background-color: #45a049;
}

.btn-delete {
    background-color: #f44336;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-delete:hover {
    background-color: #e53935;
}
</style>
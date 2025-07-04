<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';
import { LMap, LTileLayer } from '@vue-leaflet/vue-leaflet'

const leafletMap = ref(null);
const locationStore = useLocationStore();
const center = ref([39.7443, -8.80725]);

const newLocation = reactive({
    location: '',
    direction: '',
    latitude: '',
    longitude: '',
    limite: '',
});

const directions = reactive([
    { name: 'Norte', id: '1' },
    { name: 'Sul', id: '2' },
    { name: 'Este', id: '3' },
    { name: 'Oeste', id: '4' },
    { name: 'Noroeste', id: '5' },
    { name: 'Sudeste', id: '6' },
]);

function createLocation() {
    if (!newLocation.location || !newLocation.direction || !newLocation.latitude || !newLocation.longitude || !newLocation.limite) {
        const missingFields = [
            !newLocation.location ? 'Local' : '',
            !newLocation.direction ? 'Direção' : '',
            !newLocation.latitude ? 'Latitude' : '',
            !newLocation.longitude ? 'Longitude' : '',
            !newLocation.limite ? 'Limite de velocidade' : '',
        ].filter(Boolean).join(', ');

        toast({
            title: 'Campos obrigatórios vazios.',
            description: `Por preencher: ${missingFields}`,
            variant: 'destructive',
        });
        return;
    }

    locationStore.addLocation(newLocation.location, newLocation.direction, newLocation.limite, newLocation.latitude, newLocation.longitude)
        .then(() => {
            toast({
                title: 'Sucesso',
                description: `Localização ${newLocation.location} criada com sucesso!`,
            });
            newLocation.location = '';
            newLocation.direction = '';
            newLocation.latitude = '';
            newLocation.longitude = '';
            newLocation.limite = '';
        })
        .catch(error => {
            console.error('Erro ao criar localização:', error);
            toast({
                title: 'Erro',
                description: 'Ocorreu um erro ao criar a localização. Tente novamente.',
                variant: 'destructive',
            });
        });
}

function decimalToDms(decimalCoord) {
    decimalCoord = Number(decimalCoord);
    if (typeof decimalCoord !== 'number') {
        console.error('Invalid input: expected a number');
        return null;
    }

    const isNegative = decimalCoord < 0;
    const absoluteCoord = Math.abs(decimalCoord);

    const degrees = Math.floor(absoluteCoord);
    const minutes = Math.floor((absoluteCoord - degrees) * 60);
    const seconds = ((absoluteCoord - degrees) * 60 - minutes) * 60;

    const direction = isNegative ? (decimalCoord < 0 ? 'S' : 'W') : (decimalCoord > 0 ? 'N' : 'E');

    return `${degrees}° ${minutes}' ${seconds.toFixed(2)}" ${direction}`;
}

function onMapClick(e) {
    const { lat, lng } = e.latlng;
    newLocation.latitude = decimalToDms(lat.toFixed(6));
    newLocation.longitude = decimalToDms(lng.toFixed(6));
}
</script>

<template>
    <h1 class="dashboard-title">Criar Localização</h1>
    <div class="create-location">
        <div class="form-group">
            <div class="form-field">
                <label>Local:</label>
                <input v-model="newLocation.location" />
            </div>

            <div class="form-field">
                <label>Direção:</label>
                <select v-model="newLocation.direction">
                    <option disabled value="">Selecione a direção</option>
                    <option v-for="direction in directions" :key="direction.id" :value="direction.name">
                        {{ direction.name }}
                    </option>
                </select>
            </div>
            <div class="form-field">
                <label>Limite de velocidade (km/h):</label>
                <input v-model="newLocation.limite" type="number" />
            </div>
            <div class="form-row">
                <div class="form-field">
                    <label>Latitude*:</label>
                    <input v-model="newLocation.latitude" readonly />
                </div>
                <div class="form-field">
                    <label>Longitude*:</label>
                    <input v-model="newLocation.longitude" readonly />
                </div>
            </div>
            <div class="map-container">
                <l-map ref="leafletMap" :zoom="14" :center="center" style="height: 800px; width: 1500px"
                    @click="onMapClick">
                    <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution="&copy; OpenStreetMap contributors" />
                </l-map>
            </div>

            <div class="form-actions">
                <button @click="createLocation">Criar</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.create-location {
    margin-top: 2.5rem;
    padding: 1.5rem;
    background-color: #1C2541;
    border-radius: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    color: white;
}

.dashboard-title {
    font-size: 1.75rem;
    font-weight: bold;
    color: #5BC0BE;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #5BC0BE;
    padding-bottom: 0.5rem;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.form-row {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

@media (min-width: 768px) {
    .form-row {
        flex-direction: row;
    }
}

.form-field label {
    display: block;
    margin-bottom: 0.25rem;
    color: #B0BEC5;
    font-size: 0.875rem;
}

.form-field input,
.form-field select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border-radius: 0.5rem;
    border: 1px solid #5BC0BE;
    background-color: #0B132B;
    color: white;
    font-size: 0.875rem;
}

.form-field select option {
    background-color: #1C2541;
    color: white;
}

.form-actions {
    display: flex;
    justify-content: flex-end;
}

.form-actions button {
    background-color: #5BC0BE;
    color: #0B132B;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    border-radius: 0.5rem;
    transition: background-color 0.3s ease;
    border: none;
    cursor: pointer;
}

.form-actions button:hover {
    background-color: #3A506B;
}

.map-container {
    height: 500px;
    margin-top: 1rem;
    border-radius: 12px;
    overflow: hidden;
    z-index: 0;
    /*para garantir que o mapa não se meta em cima da navbar e toast*/
}

.leaflet-container {
    z-index: 0 !important;
    /*para garantir que o mapa não se meta em cima da navbar e toast*/
}

.leaflet-pane,
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-popup {
    z-index: 0 !important;
    /*para garantir que o mapa não se meta em cima da navbar e toast*/
}
</style>
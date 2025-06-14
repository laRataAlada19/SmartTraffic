<script setup>
import { ref, onMounted, watch, inject } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';
import LocationUpdate from './LocationUpdate.vue';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';
import { useErrorStore } from '@/stores/error';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import { LMap, LTileLayer, LCircleMarker, LPopup } from '@vue-leaflet/vue-leaflet'

const locationStore = useLocationStore();
const storeError = useErrorStore();
const alertDialog = inject('alertDialog')
const storeAuth = useAuthStore();
const props = defineProps({
    id: Number,
    edit: Boolean
});
const locationId = ref(props.id);
const locationDetails = ref(null);
const granularity = ref(3); //default diario
const showUpdateForm = ref(false);
const startDate = ref('2025-05-01');
const endDate = ref('2025-05-08');
const selectedCharts = ref([]);
const center = ref([])

function dmsToDecimal(coordStr) {
    if (typeof coordStr !== 'string') {
        return null;
    }

    coordStr = coordStr
        .trim()
        .replace(/º/g, '°')
        .replace(/[’′]/g, "'")
        .replace(/″/g, '"');

    const dmsPattern = /(\d+)[°\s]+(\d+)?['\s]*([\d.]+)?["\s]*([NSEW])/i;
    const match = coordStr.match(dmsPattern);

    if (match) {
        const degrees = parseFloat(match[1]);
        const minutes = parseFloat(match[2] || 0);
        const seconds = parseFloat(match[3] || 0);
        const direction = match[4].toUpperCase();

        let decimal = degrees + minutes / 60 + seconds / 3600;
        if (direction === 'S' || direction === 'W') {
            decimal *= -1;
        }
        return decimal;
    }

    const num = parseFloat(coordStr);
    return isNaN(num) ? null : num;
}

const changeGranularity = (selectedGranularity) => {
    granularity.value = selectedGranularity;
};

function deleteConfirmed(id) {
    storeError.resetMessages()
    locationStore.deleteLocation(id)
        .then(() => {
            //redirect to a diferente page after deletion
            router.push({ name: 'Locations' });
            toast({
                title: 'Sucesso',
                description: 'Localização apagada com sucesso!',
            });
        })
        .catch((error) => {
            storeError.setError(error)
        })
}

function deleteLocation(id, name) {
    alertDialog.value.open(() => deleteConfirmed(id), 'Tem a certeza?', 'Cancelar', `Sim, apagar a localização ${name}`,
        `Ao apagar este localização, seram apagdos todos os dados realtivos a mesma.`)
}

const toggleUpdateForm = () => {
    showUpdateForm.value = !showUpdateForm.value;
};

const cancelUpdate = (canceledForm) => {
    showUpdateForm.value = canceledForm.value;
};

watch([locationDetails, showUpdateForm], ([newLocation, newShowUpdate]) => {
    //carregar o mapa quando a localização ou o estado do formulário de atualização mudar
    if (newLocation && !newShowUpdate) {
        center.value = [dmsToDecimal(locationDetails.value.latitude), dmsToDecimal(locationDetails.value.longitude)];
    }
});

onMounted(async () => {
    try {
        locationDetails.value = await locationStore.fetchLocationById(locationId.value);

        if (props.edit === true) {
            showUpdateForm.value = true;
        }

        const tables = await storeAuth.getTables();
        if (tables && tables.tables && tables.tables.Location) {
            selectedCharts.value = tables.tables.Location;
        }
        () => locationDetails,
            (newVal) => {
                if (newVal) {
                    nextTick(() => {
                        const map = this.$refs.leafletMap?.mapObject
                        if (map) {
                            map.invalidateSize();
                        }
                    });
                }
            },
            { immediate: true }
    } catch (error) {
        console.error('Error fetching location details:', error);
        toast({
            title: 'Erro',
            description: 'Ocorreu um erro ao carregar os detalhes da localização.',
            variant: 'destructive',
        });
    }
});
</script>

<template>
    <div v-if="locationDetails" class="location-container">
        <h1 class="dashboard-title">Informação da Localização</h1>
        <div v-if="showUpdateForm">
            <LocationUpdate :location="locationDetails" @cancelUpdate="cancelUpdate" />
        </div>
        <div v-else>
            <header class="location-header">
                <p><strong>Localização:</strong> {{ locationDetails.location }}</p>
                <p><strong>Coordenadas geográficas:</strong></p>
                <p class="coordinate">Latitude: {{ locationDetails.latitude }}</p>
                <p class="coordinate">Longitude: {{ locationDetails.longitude }}</p>
                <p><strong>Direção da câmara:</strong> {{ locationDetails.direction }}</p>
                <div class="map-container">
                    <l-map ref="leafletMap" :zoom="14" :center="center" style="height: 100%;">
                        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution="&copy; OpenStreetMap contributors" />
                        <l-circle-marker v-for="(entry, i) in filteredData" :key="i"
                            :lat-lng="[entry.latitude, entry.longitude]" :radius="5" color="blue" fill
                            fill-opacity="0.6">
                            <l-popup>
                                <p><strong>{{ entry.full_date }} {{ entry.hour }}:{{ entry.minute }}</strong></p>
                                <p>Total: {{ total(entry) }}</p>
                            </l-popup>
                        </l-circle-marker>
                    </l-map>
                </div>
                <div class="btn-actions">
                    <button class="btn btn-edit" @click="toggleUpdateForm">Editar</button>
                    <button class="btn btn-delete"
                        @click="deleteLocation(locationDetails.location_id, locationDetails.location)">
                        Eliminar
                    </button>
                </div>
            </header>
        </div>
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
                <label><input type="radio" value="1" v-model="granularity" @change="changeGranularity(1)" /> Por
                    mês</label>
                <label><input type="radio" value="2" v-model="granularity" @change="changeGranularity(2)" /> Por
                    semana</label>
                <label><input type="radio" value="3" v-model="granularity" @change="changeGranularity(3)" /> Por
                    dia</label>
                <label><input type="radio" value="4" v-model="granularity" @change="changeGranularity(4)" /> Por
                    hora</label>
            </div>
            <div v-if="selectedCharts.length > 0" class="charts-wrapper">
                <h2>Gráficos Selecionados</h2>
                <ChartDisplay :selectedCharts="selectedCharts" />
            </div>
            <div v-else>
                <p>Nenhum gráfico selecionado.</p>
            </div>
        </section>
    </div>

    <div v-else>
        <p>A carregar os detalhes da localização...</p>
    </div>
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

.location-container {
    background-color: #0B132B;
    color: #ffffff;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
}

.location-header {
    background-color: #1C2541;
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.location-header h2 {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}

.coordinate {
    margin-left: 1.5rem;
    font-size: 1rem;
}

.map-container {
    height: 500px;
    margin-top: 1rem;
    border-radius: 12px;
    overflow: hidden;
}

.btn-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 1rem;
    gap: 1rem;
}

.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.btn-edit {
    background-color: #4CAF50;
    color: white;
}

.btn-edit:hover {
    background-color: #45a049;
}

.btn-delete {
    background-color: #f44336;
    color: white;
}

.btn-delete:hover {
    background-color: #e53935;
}

.statistics {
    background-color: #1C2541;
    padding: 2rem;
    border-radius: 12px;
}

.statistics h2 {
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
}

.controls {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}

.controls input {
    padding: 0.4rem 0.6rem;
    border-radius: 6px;
    border: none;
}

.granularity-options {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    margin: 1rem 0;
}

.granularity-options label {
    font-size: 0.95rem;
    cursor: pointer;
}

.charts-wrapper {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #0F1A35;
    border-radius: 10px;
}
</style>
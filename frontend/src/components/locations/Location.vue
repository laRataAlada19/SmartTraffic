<script setup>
import { ref, onMounted, watch, inject } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';
import LocationUpdate from './LocationUpdate.vue';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';
import { useErrorStore } from '@/stores/error';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';

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

const loadGoogleMaps = () => {
    return new Promise((resolve) => {
        if (window.google && window.google.maps) {
            resolve(window.google.maps);
        } else {
            const script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyAcCakaJA9IdVRuRa8xaHEJdhpp75qkOwU`;
            script.async = true;
            script.defer = true;
            script.onload = () => {
                resolve(window.google.maps);
            };
            document.head.appendChild(script);
        }
    });
};

const initMap = async () => {
    const googleMaps = await loadGoogleMaps();

    const map = new googleMaps.Map(document.getElementById('map'), {
        center: {
            lat: dmsToDecimal(locationDetails.value.latitude),
            lng: dmsToDecimal(locationDetails.value.longitude),
        },
        zoom: 15,
    });

    // Import the marker library for AdvancedMarkerElement
    const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');

    // Use the new marker class
    new AdvancedMarkerElement({
        map: map,
        position: {
            lat: dmsToDecimal(locationDetails.value.latitude),
            lng: dmsToDecimal(locationDetails.value.longitude),
        },
        title: locationDetails.value.location,
    });
};

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

watch([locationDetails, showUpdateForm], ([newLocation, newShowUpdate]) => { //carregar o mapa quando a localização ou o estado do formulário de atualização mudar
    if (newLocation && !newShowUpdate) {
        initMap();
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
    <br>
    <br>
    <br>
    <br>

    <div v-if="locationDetails" class="bg-white rounded-lg shadow p-4">
        <div v-if="showUpdateForm">
            <LocationUpdate :location="locationDetails" @cancelUpdate="cancelUpdate" />
        </div>
        <div v-else>
            <header>
                <h2>Informação da Localização</h2>
                <p><strong>Localização:</strong> {{ locationDetails.location }}</p>
                <p><strong>Coordenadas geográficas:</strong></p>
                <p class="latitude">Latitude: {{ locationDetails.latitude }}</p>
                <p class="longitude">Longitude: {{ locationDetails.longitude }}</p>
                <p><strong>Direção da câmara:</strong> {{ locationDetails.direction }}</p>
                <div id="map" style="height: 400px; width: 100%; margin-top: 20px;"></div>
                <div class="btn-actions">
                    <button class="btn-edit" @click="toggleUpdateForm">Editar</button>
                    <button class="btn-delete"
                        @click="deleteLocation(locationDetails.location_id, locationDetails.location)">Eliminar</button>
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
    margin-left: 300px;
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
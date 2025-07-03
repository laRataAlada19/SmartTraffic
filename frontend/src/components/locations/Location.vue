<script setup>
import { ref, onMounted, watch, inject, computed } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';
import LocationUpdate from './LocationUpdate.vue';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';
import { useErrorStore } from '@/stores/error';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import { LMap, LTileLayer, LCircleMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import * as XLSX from 'xlsx';

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
const startDate = ref(new Date().toISOString().split('T')[0]); // Data atual no formato YYYY-MM-DD
const endDate = ref(new Date().toISOString().split('T')[0]); // Data atual no formato YYYY-MM-DD
//const selectedCharts = ref([]);//AQUI
const center = ref([])
const chartRef = ref(null);

//AQUI
const selectedCharts = ref([
    'LineChart',
    'BarChart',
    'PieChart'
])

function exportExcel() {
    if (!chartRef.value || !locationDetails.value) return;

    const exportData = chartRef.value.getExportData();
    const { charts } = exportData;

    const wb = XLSX.utils.book_new();

    // Adiciona folha com metadados da localização
    const locationSheetData = [
        ['Nome da Localização', locationDetails.value.location],
        ['Latitude', locationDetails.value.latitude],
        ['Longitude', locationDetails.value.longitude],
        ['Câmara', locationDetails.value.camera],
        ['Direção', locationDetails.value.direction]
    ];
    const locationSheet = XLSX.utils.aoa_to_sheet(locationSheetData);
    XLSX.utils.book_append_sheet(wb, locationSheet, 'Localização');

    // Adiciona uma folha por gráfico selecionado
    charts.forEach(chart => {
        const sheet = XLSX.utils.json_to_sheet(chart.data);
        XLSX.utils.book_append_sheet(wb, sheet, chart.name.substring(0, 31)); // Nome da aba até 31 chars
    });

    XLSX.writeFile(wb, `export_${locationDetails.value.location}.xlsx`);
}

function exportCSV() {
    if (!chartRef.value || !locationDetails.value) return;

    const exportData = chartRef.value.getExportData();
    const { charts } = exportData;

    let csvContent = '';

    csvContent += `Campo,Valor\n`;
    csvContent += `Nome da Localização,"${locationDetails.value.location}"\n`;
    csvContent += `Latitude,"${locationDetails.value.latitude}"\n`;
    csvContent += `Longitude,"${locationDetails.value.longitude}"\n`;
    csvContent += `Câmara,"${locationDetails.value.camera}"\n`;
    csvContent += `Direção,"${locationDetails.value.direction}"\n\n`;

    charts.forEach(chart => {
        if (!chart.data || chart.data.length === 0) return;

        csvContent += `\n---------------------\n`;
        csvContent += `Gráfico: "${chart.name}"\n`;

        // Cabeçalhos
        const headers = Object.keys(chart.data[0]);
        csvContent += headers.join(',') + '\n';

        // Dados
        chart.data.forEach(row => {
            const rowValues = headers.map(key =>
                `"${String(row[key]).replace(/"/g, '""')}"`
            );
            csvContent += rowValues.join(',') + '\n';
        });

        csvContent += '\n'; // Espaço entre gráficos
    });

    // 📥 Download do CSV
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const safeLocationName = locationDetails.value.location.replace(/[^a-zA-Z0-9]/g, '_');
    a.href = url;
    a.download = `export_${safeLocationName}.csv`;
    a.click();
    URL.revokeObjectURL(url);
}

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
        <LocationUpdate v-if="showUpdateForm" :location="locationDetails" @cancelUpdate="cancelUpdate" />
        <div v-else>
            <h1 class="dashboard-title">Informação da Localização</h1>
            <div class="info-card">
                <div class="info-grid">
                    <div>
                        <h2>Localização</h2>
                        <p>{{ locationDetails.location }}</p>
                    </div>
                    <div>
                        <h2>Coordenadas</h2>
                        <p>Latitude: {{ locationDetails.latitude }}</p>
                        <p>Longitude: {{ locationDetails.longitude }}</p>
                    </div>
                    <div>
                        <h2>Designação da Câmara</h2>
                        <p>{{ locationDetails.camera }}</p>
                    </div>
                    <div>
                        <h2>Direção da Câmara</h2>
                        <p>{{ locationDetails.direction }}</p>
                    </div>
                </div>

                <div class="map-container">
                    <l-map ref="leafletMap" :zoom="14" :center="center" style="height: 100%;">
                        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution="&copy; OpenStreetMap contributors" />
                    </l-map>
                </div>

                <div class="btn-actions">
                    <button class="btn btn-edit" @click="toggleUpdateForm">Editar</button>
                    <button class="btn btn-delete"
                        @click="deleteLocation(locationDetails.location_id, locationDetails.location)">
                        Eliminar
                    </button>
                </div>
            </div>
            <h1 class="dashboard-title">Estatísticas</h1>

        <section class="statistics-card">
            <div class="statistics-header">
                <h2>Granularidade Temporal</h2>
                <div class="date-range">
                    <div class="date-field">
                        <label for="start">De</label>
                        <input id="start" type="date" v-model="startDate" />
                    </div>
                    <div class="date-field">
                        <label for="end">Até</label>
                        <input id="end" type="date" v-model="endDate" />
                    </div>
                </div>
            </div>

            <div class="granularity-buttons">
                <button @click="changeGranularity(1)" :class="{ active: granularity === 1 }">Horário</button>
                <button @click="changeGranularity(2)" :class="{ active: granularity === 2 }">Diário</button>
                <button @click="changeGranularity(3)" :class="{ active: granularity === 3 }">Semanal</button>
                <button @click="changeGranularity(4)" :class="{ active: granularity === 4 }">Mensal</button>
            </div>

            <div v-if="selectedCharts.length > 0" class="charts-wrapper">
                <h2>Gráficos Selecionados</h2>
                <ChartDisplay ref="chartRef" :selectedCharts="selectedCharts" />
            </div>
            <div v-else class="no-charts">
                <p>Nenhum gráfico selecionado.</p>
            </div>
            <div class="btn-actions export-buttons">
                <button class="btn btn-edit" @click="exportExcel">Exportar Excel</button>
                <button class="btn btn-edit" @click="exportCSV">Exportar CSV</button>
            </div>
        </section>
    </div>
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

.info-card {
    background-color: #1C2541;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.info-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    margin-bottom: 1.5rem;
}

.info-grid>div {
    flex: 1;
    min-width: 200px;
}

.info-grid h2 {
    font-size: 1.2rem;
    color: #5BC0BE;
    margin-bottom: 0.5rem;
}

.location-container {
    background-color: #0B132B;
    color: #ffffff;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
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

.charts-wrapper {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #0F1A35;
    border-radius: 10px;
}

.granularity-buttons {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.granularity-buttons button {
    background-color: #1C2541;
    color: white;
    padding: 8px 12px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background 0.3s;
}

.granularity-buttons button:hover {
    background-color: #3A506B;
}

.granularity-buttons .active {
    background-color: #5BC0BE;
    color: #0B132B;
    font-weight: bold;
}

.statistics-card {
    background-color: #1C2541;
    padding: 2rem;
    border-radius: 12px;
    margin-top: 2rem;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.statistics-header {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.statistics-header h2 {
    font-size: 1.4rem;
    color: #5BC0BE;
    margin-bottom: 0.5rem;
}

.date-range {
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
}

.date-field {
    display: flex;
    flex-direction: column;
}

.date-field label {
    font-size: 0.9rem;
    margin-bottom: 0.25rem;
}

.date-field input {
    padding: 8px;
    background-color: #0B132B;
    color: #FFFFFF;
    border: 1px solid #5BC0BE;
    border-radius: 5px;
    font-size: 1rem;
}

.no-charts {
    color: #B0BEC5;
    margin-top: 1rem;
}

.export-buttons {
    justify-content: center;
    /* Centraliza os botões */
    margin-top: 2rem;
}
</style>
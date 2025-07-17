<script setup>
import { ref, onMounted, watch, inject, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';
import { useErrorStore } from '@/stores/error';
import ChartDisplay from '@/components/charts/ChartDisplay.vue';
import { LMap, LTileLayer } from '@vue-leaflet/vue-leaflet'
import * as XLSX from 'xlsx';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import logoImgPath from '@/assets/smart-traffic-logo.png';

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
const granularity = ref(3);
const showUpdateForm = ref(false);
const startDate = ref(new Date().toISOString().split('T')[0]); 
const endDate = ref(new Date().toISOString().split('T')[0]); 
const selectedCharts = ref([]);
const center = ref([])
const chartRef = ref(null);

const directions = reactive([
    { name: 'Norte', id: '1' },
    { name: 'Sul', id: '2' },
    { name: 'Este', id: '3' },
    { name: 'Oeste', id: '4' },
    { name: 'Noroeste', id: '5' },
    { name: 'Sudeste', id: '6' },
]);

function exportExcel() {
    if (!chartRef.value || !locationDetails.value) return;

    const { charts } = chartRef.value.getExportData();
    const location = locationDetails.value;

    const workbook = XLSX.utils.book_new();

    const locationData = [
        ['Nome da Localização', location.location],
        ['Latitude', location.latitude],
        ['Longitude', location.longitude],
        ['Limite de Velocidade', `${location.limite} km/h`],
        ['Direção', location.direction],
    ];
    const locationSheet = XLSX.utils.aoa_to_sheet(locationData);
    XLSX.utils.book_append_sheet(workbook, locationSheet, 'Localização');

    charts.forEach(({ name, data }) => {
        if (!data || data.length === 0) return;
        const sheet = XLSX.utils.json_to_sheet(data);
        XLSX.utils.book_append_sheet(workbook, sheet, name.substring(0, 31));
    });

    const filename = `exportExcel_${location.location.replace(/[^a-zA-Z0-9]/g, '_')}.xlsx`;
    XLSX.writeFile(workbook, filename);
    toast({
        title: 'Sucesso',
        description: `Localização ${location.location} exportada para Excel com sucesso!`,
    });
}

function exportCSV() {
    if (!chartRef.value || !locationDetails.value) return;

    const { charts } = chartRef.value.getExportData();
    const location = locationDetails.value;

    const metadata = [
        ['Campo', 'Valor'],
        ['Nome da Localização', location.location],
        ['Latitude', location.latitude],
        ['Longitude', location.longitude],
        ['Limite de Velocidade', `${location.limite} km/h`],
        ['Direção', location.direction],
    ];

    let csvContent = metadata.map(row =>
        row.map(val => `"${String(val).replace(/"/g, '""')}"`).join(',')
    ).join('\n');

    csvContent += '\n\n';

    charts.forEach(({ name, data }) => {
        if (!data || data.length === 0) return;

        csvContent += `"Gráfico: ${name}"\n`;

        const headers = Object.keys(data[0]);
        csvContent += headers.map(h => `"${h}"`).join(',') + '\n';

        data.forEach(row => {
            const values = headers.map(key =>
                `"${String(row[key]).replace(/"/g, '""')}"`
            );
            csvContent += values.join(',') + '\n';
        });

        csvContent += '\n'; 
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    const safeFilename = `exportCSV_${location.location.replace(/[^a-zA-Z0-9]/g, '_')}.csv`;
    link.href = url;
    link.download = safeFilename;
    link.click();

    URL.revokeObjectURL(url);
    toast({
        title: 'Sucesso',
        description: `Localização ${location.location} exportada para CSV com sucesso!`,
    });
}

async function exportPDF() {
    if (!chartRef.value || !locationDetails.value) return;

    const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    const pageWidth = doc.internal.pageSize.getWidth();

    const loadImageToDataUrl = (src) => {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            img.onload = () => {
                const canvas = document.createElement('canvas');
                canvas.width = img.width;
                canvas.height = img.height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                try {
                    const dataUrl = canvas.toDataURL('image/png');
                    resolve(dataUrl);
                } catch (e) {
                    reject(e);
                }
            };
            img.onerror = (e) => reject(e);
            img.src = src;
        });
    };

    let logoDataUrl;
    try {
        logoDataUrl = await loadImageToDataUrl(logoImgPath);
    } catch (e) {
        console.error('Error loading logo:', e);
        logoDataUrl = null;
    }

    doc.setFillColor(33, 150, 243); 
    doc.rect(0, 0, pageWidth, 20, 'F');

    if (logoDataUrl) {
        doc.addImage(logoDataUrl, 'PNG', pageWidth - 40, 1.6, 20, 17);
    } else {
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(10);
        doc.text('Logo not available', pageWidth - 50, 15);
    }

    doc.setTextColor(255, 255, 255); 
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('Detalhes da Localização', 10, 13);

    doc.setTextColor(0, 0, 0);
    doc.setFontSize(11);
    doc.setFont('helvetica', 'normal');

    let y = 30;
    const metadata = [
        [`Nome:`, locationDetails.value.location],
        [`Latitude:`, locationDetails.value.latitude],
        [`Longitude:`, locationDetails.value.longitude],
        [`Limite de Velocidade:`, `${locationDetails.value.limite} km/h`],
        [`Direção:`, locationDetails.value.direction],
    ];

    metadata.forEach(([label, value]) => {
        doc.setFont('helvetica', 'bold');
        doc.text(label, 10, y);
        doc.setFont('helvetica', 'normal');
        doc.text(String(value), 60, y);
        y += 7;
    });

    doc.setDrawColor(200);
    doc.line(10, y + 2, pageWidth - 10, y + 2);
    y += 15;

    let x = 10;
    const imgWidth = 85;
    const imgHeight = 60;
    let chartCount = 0;

    const chartElements = chartRef.value?.$el?.querySelectorAll('canvas');
    if (!chartElements || chartElements.length === 0) {
        console.warn("No canvas elements found inside ChartDisplay.");
        return;
    }

    for (const canvas of chartElements) {
        const imgData = canvas.toDataURL('image/png');
        const chartName = `Gráfico ${chartCount + 1}`;

        doc.setFontSize(12);
        doc.setFont('helvetica', 'bold');
        doc.text(chartName, x, y - 4);

        doc.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight);

        doc.setDrawColor(180);
        doc.rect(x, y, imgWidth, imgHeight);

        chartCount++;

        if (chartCount % 2 === 0) {
            x = 10;
            y += imgHeight + 20;
        } else {
            x += imgWidth + 10;
        }

        if (y + imgHeight > 260) {
            const pageNumber = doc.internal.getNumberOfPages();
            doc.setFontSize(10);
            doc.text(`Página ${pageNumber}`, pageWidth - 30, 290);

            doc.addPage();
            x = 10;
            y = 20;
        }
    }

    const currentPage = doc.internal.getNumberOfPages();
    doc.setPage(currentPage);
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text(`Exportado em: ${new Date().toLocaleString()}`, 10, 290);
    doc.text(`Página ${currentPage}`, pageWidth - 30, 290);

    const safeLocationName = locationDetails.value.location.replace(/[^a-zA-Z0-9]/g, '_');
    doc.save(`exportPDF_${safeLocationName}.pdf`);
    toast({
        title: 'Sucesso',
        description: `Localização ${locationDetails.value.location} exportada para PDF com sucesso!`,
    });
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

const changeGranularity = (selectedGranularity) => {
    granularity.value = selectedGranularity;
};

function deleteConfirmed(id) {
    storeError.resetMessages()
    locationStore.deleteLocation(id)
        .then(() => {
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

async function updateLocation(location) {
    try {
        await locationStore.updateLocation(location.location_id, location);
        toast({
            title: 'Sucesso',
            description: `Localização ${location.location} atualizada com sucesso!`,
        });
        toggleUpdateForm(false); 
    } catch (error) {
        console.error('Erro ao atualizar localização:', error);
        toast({
            title: 'Erro',
            description: 'Ocorreu um erro ao atualizar a localização. Tente novamente.',
            variant: 'destructive',
        });
    }
}

const toggleUpdateForm = (aux) => {
    showUpdateForm.value = aux
};

function onMapClick(e) {
    const { lat, lng } = e.latlng;
    locationDetails.value = {
        ...locationDetails.value, 
        latitude: decimalToDms(lat.toFixed(6)), 
        longitude: decimalToDms(lng.toFixed(6)), 
    };
}

watch(showUpdateForm, (newShowUpdate) => {
    if (newShowUpdate && locationDetails.value) {
        center.value = [dmsToDecimal(locationDetails.value.latitude), dmsToDecimal(locationDetails.value.longitude)];
    }
});

onMounted(async () => {
    try {
        locationDetails.value = await locationStore.fetchLocationById(locationId.value);

        center.value = [
            dmsToDecimal(locationDetails.value.latitude),
            dmsToDecimal(locationDetails.value.longitude)
        ];


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
        <div v-if="!showUpdateForm">
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
                        <h2>Direção da Câmara</h2>
                        <p>{{ locationDetails.direction }}</p>
                    </div>
                    <div>
                        <h2>Limite Velocidade</h2>
                        <p>{{ locationDetails.limite }} km/h</p>
                    </div>
                </div>

                <div class="map-container">
                    <l-map ref="leafletMap" :zoom="14" :center="center" style="height: 100%;">
                        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution="&copy; OpenStreetMap contributors" />
                    </l-map>
                </div>

                <div class="btn-actions">
                    <button class="btn btn-edit" @click="toggleUpdateForm(true)">
                        Editar
                    </button>
                    <button class="btn btn-delete"
                        @click="deleteLocation(locationDetails.location_id, locationDetails.location)">
                        Eliminar
                    </button>
                </div>
            </div>
        </div>
        <div v-else>
            <h1 class="dashboard-title">Atualizar Localização</h1>
            <div class="info-card">
                <div class="info-grid">
                    <div class="field-group">
                        <h2>Localização</h2>
                        <input id="location" v-model="locationDetails.location" />
                    </div>
                    <div class="field-group">
                        <h2>Coordenadas</h2>
                        <p>Latitude: <input v-model="locationDetails.latitude" /></p>
                        <p>Longitude:<input v-model="locationDetails.longitude" /></p>
                    </div>
                    <div class="field-group">
                        <h2>Direção da Câmara</h2>
                        <select v-model="locationDetails.direction">
                            <option disabled value="">Selecione a direção</option>
                            <option v-for="direction in directions" :key="direction.id" :value="direction.name">
                                {{ direction.name }}
                            </option>
                        </select>
                    </div>
                    <div class="field-group">
                        <h2>Limite Velocidade</h2>
                        <input id="limite" v-model="locationDetails.limite" type="number" />
                    </div>
                </div>

                <div class="map-container">
                    <l-map ref="leafletMap" :zoom="14" :center="center" style="height: 100%;" @click="onMapClick">
                        <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution="&copy; OpenStreetMap contributors" />
                    </l-map>
                </div>

                <div class="btn-actions">
                    <button class="btn btn-edit" @click="updateLocation(locationDetails)">Guardar</button>
                    <button class="btn btn-delete" @click="toggleUpdateForm(false)">
                        Cancelar
                    </button>
                </div>
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
                <button class="btn btn-edit" @click="exportPDF">Exportar PDF</button>
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
}

.leaflet-container {
    z-index: 0 !important;
}

.leaflet-pane,
.leaflet-tile,
.leaflet-marker-icon,
.leaflet-popup {
    z-index: 0 !important;
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
</style>
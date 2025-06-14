<script setup>
import { ref, computed, onMounted } from 'vue'
import { Chart } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Tooltip,
    Title,
    Legend,
    LinearScale,
} from 'chart.js'
import { ChoroplethController, GeoFeature, ProjectionScale, ColorScale } from 'chartjs-chart-geo'
import { useSharedData } from '@/components/charts/useSharedData';

ChartJS.register(
    Tooltip,
    Title,
    Legend,
    LinearScale,
    ChoroplethController,
    GeoFeature,
    ProjectionScale,
    ColorScale
)


const trafficData = ref([
    { district: 'Leiria', value: 150 },
    { district: 'Lisboa', value: 300 },
    { district: 'Porto', value: 100 },
    { district: 'Faro', value: 50 }
])

const geoJson = ref(null)
const geoReady = ref(false)


onMounted(async () => {
    const res = await fetch('https://public.opendatasoft.com/explore/dataset/georef-portugal-distrito/download/?format=geojson')
    const topoJson = await res.json()

    geoJson.value = {
        ...topoJson,
        features: topoJson.features.map(f => ({
            type: f.type,
            properties: { ...f.properties },
            geometry: JSON.parse(JSON.stringify(f.geometry))
        }))
    }

    geoReady.value = true
    console.log('Features carregadas:', geoJson.value.features.length)
})

const chartData = computed(() => {
    if (!geoJson.value) return { labels: [], datasets: [] }


    const valueMap = trafficData.value.reduce((acc, curr) => {
        acc[curr.district] = curr.value
        return acc
    }, {})


    const featuresWithValue = geoJson.value.features.map(feature => {
        const districtName = feature.properties.NOME
        return {
            ...feature,
            value: valueMap[districtName] || 0
        }
    })

    return {
        labels: [],
        datasets: [
            {
                label: 'Mapa de Portugal',
                data: featuresWithValue,
                borderColor: 'white',
                borderWidth: 1,
                showOutline: true,
                showGraticule: false,
            }
        ]
    }
})


const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    plugins: {
        title: {
            display: true,
            text: 'Mapa de Dispersão Geográfica - Tráfego'
        },
        tooltip: {
            callbacks: {
                label: ctx => {
                    const distrito = ctx.raw.properties.NOME
                    const valor = ctx.raw.value
                    return `Distrito: ${distrito} - Intensidade: ${valor}`
                }
            }
        },
        legend: {
            display: false
        }
    },
    scales: {
        projection: {
            axis: 'x',
            projection: 'mercator'
        }
    }
}
</script>
<template>
    <div class="h-[600px]">
        <Chart v-if="geoReady" :type="'choropleth'" :data="chartData" :options="chartOptions" />
    </div>
</template>
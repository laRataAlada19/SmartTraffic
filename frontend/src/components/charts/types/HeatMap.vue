<script setup>
import { ref, computed } from 'vue'
import { Chart } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Tooltip,
    Title,
    Legend,
    LinearScale,
    CategoryScale
} from 'chart.js'

import 'chartjs-chart-matrix'
import { MatrixController, MatrixElement } from 'chartjs-chart-matrix'

ChartJS.register(
    Tooltip,
    Title,
    Legend,
    LinearScale,
    CategoryScale,
    MatrixController,
    MatrixElement
)

const data1 = ref([
    { hour: 8, car: 40, motorcycle: 10, truck: 5, bus: 3 },
    { hour: 9, car: 55, motorcycle: 12, truck: 4, bus: 2 },
    { hour: 10, car: 20, motorcycle: 8, truck: 6, bus: 1 },
    { hour: 17, car: 70, motorcycle: 20, truck: 10, bus: 5 },
])

const heatmapData = computed(() => {
    const result = []
    const types = ['car', 'motorcycle', 'truck', 'bus']

    data1.value.forEach(entry => {
        types.forEach(type => {
            result.push({
                x: entry.hour,
                y: type,
                v: entry[type] || 0
            })
        })
    })

    return result
})

const backgroundColorFn = (ctx) => {
    const value = ctx.dataset.data[ctx.dataIndex].v
    const alpha = Math.min(1, value / 50)
    return `rgba(255, 99, 132, ${alpha})`
}
</script>

<template>
    <div class="h-[500px]">
        <Chart v-if="heatmapData.length" :type="'matrix'" :data="{
            labels: [],
            datasets: [{
                label: 'Heatmap por hora e tipo',
                data: heatmapData,
                backgroundColor: backgroundColorFn,
                width: () => 20,
                height: () => 20
            }]
        }" :options="{
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 0,
                    max: 23,
                    ticks: {
                        stepSize: 1,
                        callback: val => `${val}:00`
                    },
                    title: {
                        display: true,
                        text: 'Hora do Dia'
                    }
                },
                y: {
                    type: 'category',
                    labels: ['car', 'motorcycle', 'truck', 'bus'],
                    title: {
                        display: true,
                        text: 'Tipo de Veículo'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Heatmap de Tráfego por Hora e Tipo de Veículo'
                },
                tooltip: {
                    callbacks: {
                        label: ctx => `Total: ${ctx.raw.v}`
                    }
                }
            }
        }" />

    </div>
</template>

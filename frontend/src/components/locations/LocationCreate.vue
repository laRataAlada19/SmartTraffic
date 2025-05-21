<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';

const locationStore = useLocationStore();

const newLocation = reactive({
  name: '',
  direction: '',
  latitude: '',
  longitude: '',
});

const locations = reactive([
  { name: 'Norte', id: '1' },
  { name: 'Sul', id: '2' },
  { name: 'Este', id: '3' },
  { name: 'Oeste', id: '4' },
  { name: 'Noroeste', id: '5' },
  { name: 'Sudeste', id: '6' },
]);

function createLocation() {
    //
}

</script>

<template>
    <div class="mt-10 bg-white p-4 rounded-lg shadow">
        <h3 class="text-lg font-medium mb-4">Criar Localização</h3>
        <div class="space-y-4">
            <div>
                <label class="block mb-1">Local:</label>
                <input v-model="newLocation.name" class="w-full border rounded px-3 py-2" />
            </div>
            <div>
                <label class="block mb-1">Direção:</label>
                <select v-model="newLocation.direction" class="w-full border rounded px-3 py-2">
                    <option disabled value="">Selecione a direção</option>
                    <option v-for="location in locations" :key="location.id" :value="location.name">
                        {{ location.name }}
                    </option>
                </select>
            </div>
            <div class="flex gap-4">
                <div class="flex-1">
                    <label class="block mb-1">Latitude:</label>
                    <input v-model="newLocation.latitude" class="w-full border rounded px-3 py-2" />
                </div>
                <div class="flex-1">
                    <label class="block mb-1">Longitude:</label>
                    <input v-model="newLocation.longitude" class="w-full border rounded px-3 py-2" />
                </div>
            </div>
            <div class="flex justify-end">
                <button @click="createLocation" class="mt-2 bg-green-500 text-white px-4 py-2 rounded">
                    Criar
                </button>
            </div>
        </div>
    </div>
</template>
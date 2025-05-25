<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import axios from 'axios';

const locationStore = useLocationStore();

const newLocation = reactive({
  location: '',
  direction: '',
  latitude: '',
  longitude: '',
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
    if (!newLocation.location || !newLocation.direction || !newLocation.latitude || !newLocation.longitude) {
        alert('Por preencher: '. concat(
            !newLocation.location ? 'Local, ' : '',
            !newLocation.direction ? 'Direção, ' : '',
            !newLocation.latitude ? 'Latitude, ' : '',
            !newLocation.longitude ? 'Longitude' : ''
        ));
        return;
    }

    console.log('Criando localização:', newLocation);
    
    locationStore.addLocation(newLocation.location, newLocation.direction, newLocation.latitude, newLocation.longitude)
        .then(() => {
            alert('Localização criada com sucesso!');
            newLocation.location = '';
            newLocation.direction = '';
            newLocation.latitude = '';
            newLocation.longitude = '';
        })
        .catch(error => {
            console.error('Erro ao criar localização:', error);
            alert('Ocorreu um erro ao criar a localização. Tente novamente.');
        });
}

</script>

<template>
    <div class="mt-10 bg-white p-4 rounded-lg shadow">
        <h3 class="text-lg font-medium mb-4">Criar Localização</h3>
        <div class="space-y-4">
            <div>
                <label class="block mb-1">Local:</label>
                <input v-model="newLocation.location" class="w-full border rounded px-3 py-2" />
            </div>
            <div>
                <label class="block mb-1">Direção:</label>
                <select v-model="newLocation.direction" class="w-full border rounded px-3 py-2">
                    <option disabled value="">Selecione a direção</option>
                    <option v-for="direction in directions" :key="direction.id" :value="direction.name">
                        {{ direction.name }}
                    </option>
                </select>
            </div>
            <div class="flex gap-4">
                <div class="flex-1">
                    <label class="block mb-1">Latitude*:</label>
                    <input v-model="newLocation.latitude" class="w-full border rounded px-3 py-2" />
                </div>
                <div class="flex-1">
                    <label class="block mb-1">Longitude*:</label>
                    <input v-model="newLocation.longitude" class="w-full border rounded px-3 py-2" />
                </div>
            </div>
            <h3>* em formato DD ou DMS</h3>
            <div class="flex justify-end">
                <button @click="createLocation" class="mt-2 bg-green-500 text-white px-4 py-2 rounded">
                    Criar
                </button>
            </div>
        </div>
    </div>
</template>
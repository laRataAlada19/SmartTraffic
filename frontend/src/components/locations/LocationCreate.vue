<script setup>
import { ref, onMounted, reactive } from 'vue';
import { useLocationStore } from '@/stores/location';
import { toast } from '@/components/ui/toast';

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
        const missingFields = [
            !newLocation.location ? 'Local' : '',
            !newLocation.direction ? 'Direção' : '',
            !newLocation.latitude ? 'Latitude' : '',
            !newLocation.longitude ? 'Longitude' : ''
        ].filter(Boolean).join(', ');

        toast({
            title: 'Campos obrigatórios vazios.',
            description: `Por preencher: ${missingFields}`,
            variant: 'destructive',
        });
        return;
    }

    console.log('Criando localização:', newLocation);

    locationStore.addLocation(newLocation.location, newLocation.direction, newLocation.latitude, newLocation.longitude)
        .then(() => {
            toast({
                title: 'Sucesso',
                description: `Localização ${newLocation.location} criada com sucesso!`,
            });
            newLocation.location = '';
            newLocation.direction = '';
            newLocation.latitude = '';
            newLocation.longitude = '';
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
</script>

<template>
    <div class="create-location">
        <h3 class="form-title">Criar Localização</h3>
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

            <div class="form-row">
                <div class="form-field">
                    <label>Latitude*:</label>
                    <input v-model="newLocation.latitude" />
                </div>
                <div class="form-field">
                    <label>Longitude*:</label>
                    <input v-model="newLocation.longitude" />
                </div>
            </div>

            <p class="hint-text">* em formato DD ou DMS</p>

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

.form-title {
    font-size: 1.25rem;
    font-weight: 600;
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

.hint-text {
    font-size: 0.875rem;
    color: #B0BEC5;
    font-style: italic;
}
</style>
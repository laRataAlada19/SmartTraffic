<script setup>
import { ref, onMounted, inject } from 'vue';
import { useLocationStore } from '@/stores/location';
import { useErrorStore } from '@/stores/error';
import { useRouter } from 'vue-router';

const router = useRouter();
const locationStore = useLocationStore();
const alertDialog = inject('alertDialog')
const storeError = useErrorStore();
const props = defineProps({
  locations: Array
})
const availableCameras = ref({})
const selectedCamera = ref({})
const isRecording = ref({})

onMounted(async () => {
  try {
        const response = await fetch('http://localhost:5001/cameras');
        const data = await response.json();
        availableCameras.value = data;
    } catch (error) {
        console.error('Erro ao buscar câmaras:', error);
        toast({
            title: 'Erro ao listar câmaras',
            description: 'Certifique-se que o servidor local está a correr.',
            variant: 'destructive',
        });
    }
})


async function toggleRecording(location) {
  const name = selectedCamera.value[location.location_id]
  if (!name) return alert("Seleciona uma câmara")

  const action = isRecording.value[location.location_id] ? 'stop' : 'start'
  if( action === 'start' && !name) {
    alert("Por favor, seleciona uma câmara para iniciar a gravação.")
    return
  }
  if (action === 'stop' && !isRecording.value[location.location_id]) {
    alert("A gravação já está parada.")
    return
  }
  if(action === 'start') {
    alert(`A iniciar gravação na câmara ${name}...`);
    const response = await fetch(`http://localhost:5001/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          camera_name: name,
          location_id: location.location_id
        })
      });
    if(response.ok ) {
      alert(`Gravação iniciada com sucesso na câmara ${name}.`);
      isRecording.value[location.location_id] = !isRecording.value[location.location_id];
    } else if(response.status === 407){
      alert(`A gravação na câmara ${name} já está a decorrer.`);
    }
    else {
      alert(`Erro ao iniciar a gravação na câmara ${name}.`);
    }
  } else {
    if(action === 'stop') {
      const response = await fetch(`http://localhost:5001/stop`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          camera_name: name,
          location_id: location.location_id
        })
      });
    if (response.ok) {
      alert(`Gravação parada com sucesso na câmara ${name}.`);
    } else {
      alert(`Erro ao parar a gravação na câmara ${name}.`);
      console.error('Erro ao parar a gravação:', response.statusText);
    }
    isRecording.value[location.location_id] = !isRecording.value[location.location_id];
    alert(`A parar gravação na câmara ${name}...`);
  }
}
 
}

function viewLocation(location) {
  router.push({
    name: 'Location',
    params: {
      id: location.location_id
    }
  });
}

function editLocation(location) {
  router.push({
    name: 'Location',
    params: {
      id: location.location_id,
      action: 'edit'
    }
  });
}

function deleteConfirmed(id) {
  storeError.resetMessages()
  locationStore.deleteLocation(id)
    .then(() => {
      locationStore.fetchLocations()
    })
    .catch((error) => {
      storeError.setError(error)
    })
}

function deleteLocation(id, name) {
  alertDialog.value.open(() => deleteConfirmed(id), 'Tem a certeza?', 'Cancelar', `Sim, apagar a localização ${name}`,
    `Ao apagar esta localização, serão apagados todos os dados relativos à mesma.`);
}

</script>

<template>
  <div class="locations-column">
    <div class="locations-table">
      <table>
        <thead>
          <tr>
            <th>Localização</th>
            <th>Direção</th>
            <th class="text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(location, index) in locations" :key="index">
            <td>{{ location.location }}</td>
            <td>{{ location.direction }}</td>
            <td class="action-buttons">
              <button @click="viewLocation(location)">
                <img src="../icons/eye.svg" alt="eye" class="icon">
              </button>
              <button @click="editLocation(location)">
                <img src="../icons/pencil.svg" alt="pencil" class="icon">
              </button>
              <button @click="deleteLocation(location.location_id, location.location)">
                <img src="../icons/trash.svg" alt="trash" class="icon">
              </button>
              <select v-model="selectedCamera[location.location_id]">
                <option disabled value="">Seleciona a câmara</option>
                <option v-for="camera in availableCameras" :value="camera.name" :key="camera.index">{{ camera.name }}</option>
              </select>

              <button @click="toggleRecording(location)">
                {{ isRecording[location.location_id] ? 'Parar' : 'Gravar' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.locations-column {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  background-color: #1C2541;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
}

.locations-table table {
  width: 100%;
  border-collapse: collapse;
  color: #FFFFFF;
  font-size: 0.95rem;
}

.locations-table thead {
  background-color: #0B132B;
}

.locations-table th,
.locations-table td {
  border: 1px solid #3A506B;
  padding: 12px;
  text-align: left;
}

.locations-table th {
  color: #5BC0BE;
  font-weight: 600;
}

.locations-table tr:hover {
  background-color: rgba(91, 192, 190, 0.05);
}

.icon {
  width: 24px;
  height: 24px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}
</style> 
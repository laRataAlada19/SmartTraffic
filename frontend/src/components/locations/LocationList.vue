<script setup>
import { ref, onMounted, inject } from 'vue';
import { useLocationStore } from '@/stores/location';
import { useErrorStore } from '@/stores/error';
import { useRouter } from 'vue-router';
import { toast } from '@/components/ui/toast';

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
async function getStatus(location) {
  try {
    const response = await fetch(`http://localhost:5001/status`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (response.ok) {
      const data = await response.json();
      console.log(`Estado da gravação para a localização ${location.location_id}:`, data);
      if (data.status === 'Gravação em andamento') {
        toast({
          title: 'Estado da Gravação',
          description: `Gravação em andamento na localização ${data.location_id}.`,
          variant: 'info',
        });
      } else {
        toast({
          title: 'Estado da Gravação',
          description: 'Nenhuma gravação em andamento.',
          variant: 'default',
        });
      }
    } else {
      console.error('Erro ao obter o estado da gravação:', response.statusText);
      toast({
        title: 'Erro',
        description: 'Não foi possível obter o estado da gravação.',
        variant: 'destructive',
      });
    }
  } catch (error) {
    console.error('Erro de rede ao obter o estado da gravação:', error);
    toast({
      title: 'Erro de Rede',
      description: 'Ocorreu um erro ao comunicar com o servidor.',
      variant: 'destructive',
    });
  }
}

async function toggleRecording(location) {
  const name = selectedCamera.value[location.location_id];
  const action = isRecording.value[location.location_id] ? 'stop' : 'start';

  if (action === 'start' && !name) {
    toast({
      title: 'Erro',
      description: 'Por favor, seleciona uma câmara para iniciar a gravação.',
      variant: 'destructive',
    });
    return;
  }

  try {
    const response = await fetch(`http://localhost:5001/${action}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        camera_name: name,
        location_id: location.location_id,
      }),
    });

    if (response.ok) {
      toast({
        title: 'Sucesso',
        description: `Gravação ${action === 'start' ? 'iniciada' : 'parada'} com sucesso na câmara ${name}.`,
        variant: 'default',
      });
      isRecording.value[location.location_id] = !isRecording.value[location.location_id];
    } else if (response.status === 407) {
      toast({
        title: 'Aviso',
        description: `A gravação na câmara ${name} já está a decorrer.`,
        variant: 'info',
      });
    } else {
      toast({
        title: 'Erro',
        description: `Erro ao ${action === 'start' ? 'iniciar' : 'parar'} a gravação na câmara ${name}.`,
        variant: 'destructive',
      });
    }
  } catch (error) {
    toast({
      title: 'Erro de Rede',
      description: 'Ocorreu um erro ao comunicar com o servidor. Verifique sua conexão.',
      variant: 'destructive',
    });
    console.error('Erro ao comunicar com o servidor:', error);
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
    `Ao apagar este localização, serão apagados todos os dados relativos a mesma.`)
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
              <select class="custom-select" v-model="selectedCamera[location.location_id]">
                <option disabled value="">Seleciona a câmara</option>
                <option v-for="camera in availableCameras" :value="camera.name" :key="camera.index">{{ camera.name }}</option>
              </select>
              <button @click="getStatus(location)">
                <img src="../icons/refresh.svg" alt="refresh" class="icon">
              </button>

              <button
  @click="toggleRecording(location)"
  :class="['record-button', isRecording[location.location_id] ? 'stop' : '']"
>
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
.record-button {
  background-color: #5BC0BE;
  color: #0B132B;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.record-button:hover {
  background-color: #3a8d8a;
}

.record-button.stop {
  background-color: #FF4C4C;
  color: white;
}

.record-button.stop:hover {
  background-color: #cc0000;
}

.locations-column {
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  background-color: #1C2541;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);
}
.custom-select {
  background-color: #0B132B;
  color: #FFFFFF;
  border: 1px solid #3A506B;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.95rem;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  outline: none;
  transition: border-color 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

.custom-select:hover {
  border-color: #5BC0BE;
}

.custom-select:focus {
  border-color: #5BC0BE;
  box-shadow: 0 0 0 2px rgba(91, 192, 190, 0.3);
  background-color: #1C2541;
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
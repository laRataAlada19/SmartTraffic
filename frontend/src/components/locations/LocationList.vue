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
    `Ao apagar este localização, seram apagdos todos os dados realtivos a mesma.`)
}

</script>

<template>
  <div class="bg-white rounded-lg shadow p-4">
    <table class="w-full table-auto border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-100">
          <th class="border border-gray-300 px-4 py-2 text-left">Localização</th>
          <th class="border border-gray-300 px-4 py-2 text-left">Direção</th>
          <th class="border border-gray-300 px-4 py-2 text-center">Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(location, index) in locations" :key="index">
          <td class="border border-gray-300 px-4 py-2">{{ location.location }}</td>
          <td class="border border-gray-300 px-4 py-2">{{ location.direction }}</td>
          <td class="border border-gray-300 px-4 py-2 flex justify-center space-x-2">
            <button @click="viewLocation(location)">
              <img src="../icons/eye.svg" alt="eye" class="w-6 h-6">
            </button>
            <button @click="editLocation(location)">
              <img src="../icons/pencil.svg" alt="pencil" class="w-6 h-6">
            </button>
            <button @click="deleteLocation(location.location_id, location.location)">
              <img src="../icons/trash.svg" alt="trash" class="w-6 h-6">
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useLocationStore } from '@/stores/location';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const props = defineProps({
  locations: Array
})

function viewLocation(location) {
  router.push({
    name: 'Location',
    params: { id: location.location_id }
  });
}

function editLocation(location) {
  //
}

function deleteLocation(id) {
  //
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
            <button @click="deleteLocation(location.location_id)">
              <img src="../icons/trash.svg" alt="trash" class="w-6 h-6">
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
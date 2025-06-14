
import { ref, onMounted } from 'vue';
import { useFactVehicleStore } from '@/stores/factvehicle';

const sharedData = ref([]);
const isDataLoaded = ref(false);

export function useSharedData() {
  const store = useFactVehicleStore();

  const fetchData = async () => {
    if (!isDataLoaded.value) {
      sharedData.value = await store.fetchData();
      isDataLoaded.value = true;
      console.log('Dados carregados:', sharedData.value);
    }
  };

  onMounted(fetchData);

  return {
    sharedData,
    fetchData,
  };
}
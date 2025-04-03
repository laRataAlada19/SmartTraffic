import { createRouter, createWebHistory } from 'vue-router';
import LocationList from '@/components/LocationList.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LocationList,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth' 
import LocationList from '@/components/LocationList.vue';
import Login from '@/components/auth/Login.vue'

let handlingFirstRoute = true
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes:[
    {
      path: '/login',
      name: 'login',
      component: Login
    },
   {
    path: '/',
    name: 'Home',
    component: LocationList,
  },
  ]
})

router.beforeEach(async (to, from, next) => {
  const storeAuth = useAuthStore()
  if (handlingFirstRoute) { 
    handlingFirstRoute = false
    await storeAuth.restoreToken() 
  } 
  if (((to.name == 'updateTask') || (to.name == 'updateProject')) && (!storeAuth.user)) {
    next({ name: 'login' }) 
    return
  }
  next()
})

export default router;
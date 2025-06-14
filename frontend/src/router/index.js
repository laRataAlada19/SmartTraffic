import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Login from '@/components/auth/Login.vue'
import Locations from '@/components/locations/Locations.vue'
import Location from '@/components/locations/Location.vue'
import ChartSelectionPage from '@/components/charts/ChartSelectionPage.vue'
import Dasboard from '@/components/Dasboard.vue'

let handlingFirstRoute = true

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/locations',
      name: 'Locations',
      component: Locations
    },
    {
      path: '/locations/:id/:action?',
      name: 'Location',
      component: Location,
      props: route => ({
        id: parseInt(route.params.id),
        edit: route.params.action === 'edit' // true if action param is 'edit'
      })
    },
    {
      path: '/selecionarGraficos',
      name: 'selecionarGraficos',
      component: ChartSelectionPage
    },
    {
      path: '/',
      name: 'dashboard',
      component: Dasboard
    }
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

export default router

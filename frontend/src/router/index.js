import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import TaskUpdate from '@/components/tasks/TaskUpdate.vue'
import ProjectUpdate from '@/components/projects/ProjectUpdate.vue'
import ProjectCreate from '@/components/projects/ProjectCreate.vue'
import Projects from '@/components/projects/Projects.vue'

import Login from '@/components/auth/Login.vue'
import Main from '@/components/Main.vue'
import Locations from '@/components/locations/Locations.vue'
import Location from '@/components/locations/Location.vue'
import Tables from '@/components/tables/Tables.vue'
import ChartSelectionPage from '@/components/charts/ChartSelectionPage.vue'
import Dasboard from '@/components/charts/Dasboard.vue'

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
      path: '/',
      name: 'main',
      component: Main
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
      path: '/tables',
      name: 'Tables',
      component: Tables
    },
    {
      path: '/selecionarGraficos',
      name: 'selecionarGraficos',
      component: ChartSelectionPage
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dasboard
    },
    {
      path: '/tasks',
      redirect: { name: 'tasks' }
    },
    {
      path: '/tasks/:id',
      name: 'updateTask',
      component: TaskUpdate,
      props: route => ({ id: parseInt(route.params.id) })
    },
    {
      path: '/projects',
      name: 'projects',
      component: Projects
    },
    {
      path: '/projects/:id',
      name: 'updateProject',
      component: ProjectUpdate,
      props: route => ({ id: parseInt(route.params.id) })
    },
    {
      path: '/projects/new',
      name: 'createProject',
      component: ProjectCreate,
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

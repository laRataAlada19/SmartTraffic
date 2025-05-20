import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth' 
import Tasks from '@/components/tasks/Tasks.vue'
import TaskUpdate from '@/components/tasks/TaskUpdate.vue'
import ProjectUpdate from '@/components/projects/ProjectUpdate.vue'
import ProjectCreate from '@/components/projects/ProjectCreate.vue'
import Projects from '@/components/projects/Projects.vue'
import Login from '@/components/auth/Login.vue'
import Locations from '@/components/locations/Locations.vue'

let handlingFirstRoute = true

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'tasks',
      component: Locations
    },
    {
      path: '/login',
      name: 'login',
      component: Login
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
    },    
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
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

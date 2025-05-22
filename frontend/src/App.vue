<script setup>
import { onMounted, useTemplateRef, provide } from 'vue'
import { RouterView } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { useTaskStore } from '@/stores/task'
import { useAuthStore } from '@/stores/auth'
import Toaster from '@/components/ui/toast/Toaster.vue'
import GlobalAlertDialog from '@/components/common/GlobalAlertDialog.vue'

const storeProject = useProjectStore()
const storeTask = useTaskStore()
const storeAuth = useAuthStore()

onMounted(() => {

})

const alertDialog = useTemplateRef('alert-dialog')
provide('alertDialog', alertDialog)

const logoutConfirmed = () => {
  storeAuth.logout()
}


const logout = () => {
  alertDialog.value.open(logoutConfirmed, 'Logout confirmation?', 'Cancel', `Yes, I want to log out`,
    `Are you sure you want to log out? You can still access your account later with your credentials.`)
}
</script>

<template>
  <Toaster />
  <GlobalAlertDialog ref="alert-dialog"></GlobalAlertDialog>
  <div class="p-8 mx-auto max-w-3xl">
    <div class="flex justify-between">
      <img v-if="storeAuth.user" class="w-14 h-14 rounded-full" :src="storeAuth.userPhotoUrl" alt="Rounded avatar">
    </div>
    <nav style="background-color: #0B132B"
      class="bg-[#0B132B] text-white flex items-center px-2 py-1 shadow-md fixed top-0 left-0 w-full z-50 space-x-4">
      <RouterLink to="/" class="flex items-center space-x-2">
        <div class="logo-container">
          <img src="@/assets/smart-traffic-logo.png" alt="Logo"
            class="w-10 h-10 sm:w-12 sm:h-12 lg:w-16 lg:h-16 object-contain" />
        </div>
      </RouterLink>
      <RouterLink :to="{ name: 'main' }" class="text-white hover:text-green-400 transition" active-class="font-bold">
        Inicio
      </RouterLink>
      <RouterLink :to="{ name: 'selecionarGraficos' }" class="text-white hover:text-green-400 transition"
        active-class="font-bold">
        Gráficos
      </RouterLink>
      <RouterLink :to="{ name: 'Locations' }" class="text-white hover:text-green-400 transition"
        active-class="font-bold">
        Localizações
      </RouterLink>
      <RouterLink :to="{ name: 'dashboard' }" class="text-white hover:text-green-400 transition"
        active-class="font-bold">
        Dashboard
      </RouterLink>
      <span class="grow"></span>
      <RouterLink v-show="!storeAuth.user" :to="{ name: 'login' }" class="text-white hover:text-green-400 transition"
        active-class="font-bold">
        Login
      </RouterLink>
      <button v-show="storeAuth.user" @click="logout" class="text-white hover:text-green-400 transition"
        active-class="font-bold">
        Logout
      </button>
    </nav>
    <RouterView></RouterView>
  </div>
</template>

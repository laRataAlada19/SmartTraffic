<script setup>
import { onMounted, useTemplateRef, provide } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Toaster from '@/components/ui/toast/Toaster.vue'
import GlobalAlertDialog from '@/components/common/GlobalAlertDialog.vue'


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
  <div v-if="$route.name === 'login'" class="min-h-screen">
    <RouterView />
  </div>

  <div v-else class="min-h-screen bg-white">
    <Toaster />
    <GlobalAlertDialog ref="alert-dialog" />

    <nav class="bg-[#0B132B] text-white flex items-center px-6 py-3 shadow-md fixed top-0 left-0 w-full z-50">
      <RouterLink to="/" class="flex items-center space-x-2">
        <img src="@/assets/smart-traffic-logo.png" alt="Logo" class="w-8 h-8" />
      </RouterLink>

      <div class="flex space-x-8 ml-12">
        <RouterLink
          to="/"
          class="text-white hover:text-green-400 transition"
          active-class="font-bold"
        >
          Início
        </RouterLink>
        <RouterLink
          to="/tables"
          class="text-white hover:text-green-400 transition"
          active-class="font-bold"
        >
          Gráficos
        </RouterLink>
        <RouterLink
          to="/locations"
          class="text-white hover:text-green-400 transition"
          active-class="font-bold"
        >
          Localizações
        </RouterLink>
      </div>


      <div class="ml-auto flex items-center space-x-4">
        <span class="hidden sm:block text-sm">{{ storeAuth.userFirstLastName }}</span>
        <img
          v-if="storeAuth.user"
          class="w-10 h-10 rounded-full object-cover"
          :src="storeAuth.userPhotoUrl"
          alt="Avatar"
        />
        <button
          v-show="storeAuth.user"
          @click="logout"
          class="bg-gray-600 hover:bg-gray-500 text-white px-4 py-1 rounded-full text-sm"
        >
          Logout
        </button>
      </div>
    </nav>

    <div class="p-6 max-w-6xl mx-auto pt-20">
      <RouterView />
    </div>
  </div>
</template>
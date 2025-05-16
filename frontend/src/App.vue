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
  <div v-else class="p-8 mx-auto max-w-3xl">
    <Toaster />
    <GlobalAlertDialog ref="alert-dialog"></GlobalAlertDialog>


    <div class="flex justify-between">
      <h1 class="text-4xl pb-8">
        Smart Traffic {{ storeAuth.userFirstLastName ? 'of ' + storeAuth.userFirstLastName : '' }}
      </h1>
      <img v-if="storeAuth.user" class="w-14 h-14 rounded-full" :src="storeAuth.userPhotoUrl" alt="Rounded avatar" />
    </div>

    <nav class="flex space-x-1 border-b-2 border-gray-800 text-base">
      <span class="grow"></span>
      <RouterLink
        v-show="!storeAuth.user"
        :to="{ name: 'login'}"
        class="w-24 h-10 leading-10 text-center rounded-t-xl text-white bg-gray-400 hover:bg-gray-500"
        active-class="bg-gray-800"
      >
        Login
      </RouterLink>
      <button
        v-show="storeAuth.user"
        @click="logout"
        class="w-24 h-10 leading-10 text-center rounded-t-xl text-white bg-gray-400 hover:bg-gray-500"
      >
        Logout
      </button>
    </nav>

    <RouterView />
  </div>
</template>

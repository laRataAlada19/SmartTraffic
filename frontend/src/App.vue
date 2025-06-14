<script setup>
import { useTemplateRef, provide } from 'vue'
import { RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Toaster from '@/components/ui/toast/Toaster.vue'
import GlobalAlertDialog from '@/components/common/GlobalAlertDialog.vue'
import 'leaflet/dist/leaflet.css'

const storeAuth = useAuthStore()
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
  <GlobalAlertDialog ref="alert-dialog" />
  <div class="app-container">
    <!-- Navigation -->
    <nav class="navbar">
      <RouterLink to="/" class="logo-link">
        <img src="@/assets/smart-traffic-logo.png" alt="Logo" class="logo-img" />
      </RouterLink>
      <RouterLink to="/" class="nav-link" active-class="active-link">
        Dashboard
      </RouterLink>
      <RouterLink :to="{ name: 'Locations' }" class="nav-link" active-class="active-link">
        Localizações
      </RouterLink>
      <RouterLink :to="{ name: 'selecionarGraficos' }" class="nav-link" active-class="active-link">
        Configuração
      </RouterLink>
      <span class="spacer"></span>
      <RouterLink v-show="!storeAuth.user" :to="{ name: 'login' }" class="nav-link" active-class="active-link">
        Login
      </RouterLink>
      <button v-show="storeAuth.user" @click="logout" class="nav-link logout-btn">
        Logout
      </button>
    </nav>
    <!-- Main Content -->
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  background-color: #0B132B;
  color: white;
  min-height: 100vh;
}

.navbar {
  background-color: #0B132B;
  color: white;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.logo-link {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}

.logo-img {
  width: 50px;
  height: 50px;
}

.nav-link {
  margin-right: 1rem;
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #479291;
}

.active-link {
  font-weight: bold;
  color: #5BC0BE;
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font: inherit;
}

.spacer {
  flex-grow: 1;
}

.main-content {
  padding-top: 5rem;
  padding-left: 1rem;
  padding-right: 1rem;
}
</style>
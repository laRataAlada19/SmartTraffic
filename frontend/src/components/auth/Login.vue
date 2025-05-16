<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import ErrorMessage from '@/components/common/ErrorMessage.vue'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuthStore } from '@/stores/auth'
import { useErrorStore } from '@/stores/error'
import logo from '@/assets/smart-traffic-logo.png'

const router = useRouter()
const storeAuth = useAuthStore()
const storeError = useErrorStore()

const credentials = ref({
  email: '',
  password: ''
})

const login = () => {
  storeAuth.login(credentials.value)
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-white px-4">
    <Card class="w-full max-w-lg p-6 rounded-xl border-0 shadow-none bg-transparent">
      
      <div class="flex justify-center mb-8">
        <img
          :src="logo"
          alt="Smart Traffic Logo"
          class="w-40 h-40 sm:w-48 sm:h-48 rounded-2xl object-contain bg-[#0B132B] p-4"
        />
      </div>

      <CardContent class="space-y-4">
        <!-- Campo Email -->
        <div class="flex flex-col sm:flex-row items-center gap-4">
          <Label for="email" class="text-base w-24 text-center sm:text-left">User:</Label>
          <Input
            id="email"
            type="email"
            v-model="credentials.email"
            placeholder="Enter your email"
            class="rounded-full bg-gray-200 px-4 py-2 flex-1 w-full"
            autocomplete="username"
          />
        </div>
        <ErrorMessage :errorMessage="storeError.fieldMessage('email')" />

        <!-- Campo Password -->
        <div class="flex flex-col sm:flex-row items-center gap-4">
          <Label for="password" class="text-base w-24 text-center sm:text-left">Password:</Label>
          <Input
            id="password"
            type="password"
            v-model="credentials.password"
            placeholder="Enter your password"
            class="rounded-full bg-gray-200 px-4 py-2 flex-1 w-full"
            autocomplete="current-password"
          />
        </div>
        <ErrorMessage :errorMessage="storeError.fieldMessage('password')" />
      </CardContent>

      <CardFooter class="flex flex-col sm:flex-row justify-between items-center gap-4 pt-6">
        <Button
          @click="goToRegister"
          class="bg-green-400 hover:bg-green-500 text-white rounded-[12px] px-6 py-2 transition-colors duration-300 w-full sm:w-auto"
        >
          Criar Conta
        </Button>
        <Button
          @click="login"
          class="bg-gray-200 hover:bg-gray-300 text-black rounded-[12px] px-6 py-2 transition-colors duration-300 w-full sm:w-auto"
        >
          Login
        </Button>
      </CardFooter>
    </Card>
  </div>
</template>


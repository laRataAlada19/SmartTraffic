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
    <Card class="w-full max-w-md p-6 rounded-xl shadow-lg border border-blue-300">
      
      <div class="flex justify-center mb-6">
        <img
          :src="logo"
          alt="Smart Traffic Logo"
          class="w-28 h-28 rounded-xl object-contain bg-[#0B132B] p-4"
        />
      </div>


      <CardContent class="space-y-5">
        <div class="flex flex-col space-y-2">
          <Label for="email" class="text-base">User:</Label>
          <Input
            id="email"
            type="email"
            v-model="credentials.email"
            placeholder="Enter your email"
            class="rounded-full bg-gray-200 px-4 py-2 w-full"
            autocomplete="username"
          />
          <ErrorMessage :errorMessage="storeError.fieldMessage('email')" />
        </div>

        <div class="flex flex-col space-y-2">
          <Label for="password" class="text-base">Password:</Label>
          <Input
            id="password"
            type="password"
            v-model="credentials.password"
            placeholder="Enter your password"
            class="rounded-full bg-gray-200 px-4 py-2 w-full"
            autocomplete="current-password"
          />
          <ErrorMessage :errorMessage="storeError.fieldMessage('password')" />
        </div>
      </CardContent>


      <CardFooter class="flex justify-between pt-6">
        <Button
          @click="goToRegister"
          class="bg-green-400 hover:bg-green-500 text-white rounded-md px-6 py-2 transition-colors duration-300"
        >
          Criar Conta
        </Button>
        <Button
          @click="login"
          class="bg-gray-200 hover:bg-gray-300 text-black rounded-md px-6 py-2 transition-colors duration-300"
        >
          Login
        </Button>
        
      </CardFooter>
    </Card>
  </div>
</template>

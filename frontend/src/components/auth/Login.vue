<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuthStore } from '@/stores/auth'
import { useErrorStore } from '@/stores/error'
import logo from '@/assets/smart-traffic-logo.png'
import { toast } from '../ui/toast'

const router = useRouter()
const storeAuth = useAuthStore()
const storeError = useErrorStore()

const credentials = ref({
  email: '',
  password: ''
})

const cancel = () => {
  router.back()
}

const login = () => {
  storeError.clearErrors()
  storeAuth.login(credentials.value)
    .then(() => {
      toast({
        title: 'Login Successful',
        description: 'You have successfully logged in.',
        variant: 'success',
      })
      router.push({ name: 'dashboard' })
    })
    .catch((error) => {
      console.error('Login failed:', error)
      toast({
        title: 'Login Failed',
        description: 'Please check your credentials and try again.',
        variant: 'destructive',
      })
    })
}
</script>

<template>
  <Card class="w-[450px] mx-auto my-8 p-4 px-8 border-none shadow-none bg-[#1C2541]"
    style="margin-top: 100px; border-radius: 12px; box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);">
    <CardHeader>
      <div class="flex justify-center mb-6">
        <img :src="logo" alt="Smart Traffic Logo"
          class="w-40 h-40 sm:w-48 sm:h-48 rounded-2xl object-contain bg-[#0B132B] p-4" />
      </div>
    </CardHeader>

    <CardContent>
      <form>
        <div class="grid items-center w-full gap-4">
          <div class="flex flex-col space-y-1.5">
            <div class="flex items-center space-x-2">
              <Label for="email" style="color: white;">Email:</Label>
              <Input id="email" type="email" placeholder="User Email" v-model="credentials.email"
                class="rounded-full bg-gray-200 px-4 py-2 flex-1 w-full" />
            </div>
            <ErrorMessage :errorMessage="storeError.fieldMessage('email')"></ErrorMessage>
          </div>

          <div class="flex flex-col space-y-1.5">
            <div class="flex items-center space-x-2">
              <Label for="password" style="color: white;">Password:</Label>
              <Input id="password" type="password" v-model="credentials.password"
                class="rounded-full bg-gray-200 px-4 py-2 flex-1 w-full" />
            </div>
            <ErrorMessage :errorMessage="storeError.fieldMessage('password')"></ErrorMessage>
          </div>
        </div>
      </form>
    </CardContent>

    <CardFooter class="flex justify-end gap-4 pt-4">
      <Button variant="outline" @click="cancel" class="btn-outline">
        Criar Conta
      </Button>
      <Button @click="login" class="btn-primary">
        Login
      </Button>
    </CardFooter>
  </Card>
</template>

<style scoped>
.dark-card {
  background-color: #1C2541;
  border-radius: 12px;
  color: #ffffff;
  box-shadow: 0 0 10px rgba(91, 192, 190, 0.15);
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-field {
  display: flex;
  flex-direction: column;
}

.form-label {
  color: #B0BEC5;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background-color: #0B132B;
  border: 1px solid #5BC0BE;
  color: #ffffff;
  font-size: 1rem;
}

.form-input::placeholder {
  color: #B0BEC5;
}

.btn-outline {
  background-color: #4CAF50;
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-outline:hover {
  background-color: #45a049;
}

.btn-primary {
  background-color: #f44336;
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 8px;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background-color: #e53935;
}
</style>
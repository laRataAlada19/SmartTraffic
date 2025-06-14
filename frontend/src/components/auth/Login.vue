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
  storeAuth.login(credentials.value)
}
</script>

<template>
  <Card class="w-[450px] mx-auto my-8 p-4 px-8 border-none shadow-none bg-[#1C2541]"
    style="margin-top: 100px; border-radius: 12px; box-shadow: 0 0 10px rgba(91, 192, 190, 0.1);">
    <CardHeader>
      <div class="flex justify-center mb-4">
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
    <CardFooter class="flex justify-end space-x-2 px-6 pb-6">
      <Button variant="outline" @click="cancel" class="bg-green-400 text-white hover:bg-green-500">
        Criar Conta
      </Button>
      <Button @click="login" class="bg-gray-200 hover:bg-gray-300 text-black">
        Login
      </Button>
    </CardFooter>
  </Card>
</template>
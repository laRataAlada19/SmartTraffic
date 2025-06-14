import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import ErrorMessage from './components/common/ErrorMessage.vue'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
  iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
  shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Default Axios configuration
axios.defaults.baseURL = 'http://localhost:8000/api'

app.component('ErrorMessage', ErrorMessage)

app.mount('#app')

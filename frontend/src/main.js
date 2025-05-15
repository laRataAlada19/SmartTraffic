import { createApp } from 'vue';
import { createPinia } from 'pinia';
import axios from 'axios';
import App from './App.vue';
import './assets/main.css';
import router from './router'; 


const app = createApp(App);

const pinia = createPinia();

app.use(pinia);

app.use(router); // Use o router aqui

axios.defaults.baseURL = 'http://localhost:8000'; // Defina a URL base para suas requisições

app.mount('#app');
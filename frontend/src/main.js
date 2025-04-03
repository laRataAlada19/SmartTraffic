import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router'; // Certifique-se de que o caminho está correto

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);

app.use(router); // Use o router aqui

app.mount('#app');
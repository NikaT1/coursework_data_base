import { createApp } from 'vue'
import App from "@/App.vue";
import Notifications from '@kyvg/vue3-notification';
import router from "./Router.js";
import store from './store';
import PrimeVue from 'primevue/config';
import 'primevue/resources/primevue.min.css'
import 'primevue/resources/themes/saga-blue/theme.css'
import 'primeicons/primeicons.css'
import 'primeflex/primeflex.css';

const app = createApp(App);
app.use(store).use(router).use(PrimeVue).use(Notifications);
app.mount('#app');

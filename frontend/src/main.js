import { createApp } from 'vue'
import App from "@/App.vue";
import Notifications from '@kyvg/vue3-notification';
import router from "./Router.js";
import store from './store';

const app = createApp(App);
app.use(store).use(router).use(Notifications);
app.mount('#app');

import { createApp } from 'vue'
import App from "@/App.vue";
import Notifications from '@kyvg/vue3-notification';
import router from "./Router.js";
import { store } from './store';

const app = createApp(App).use(router).use(Notifications);
app.use(store);
app.config.globalProperties.$store = store;
app.mount('#app');

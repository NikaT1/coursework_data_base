import * as Vue from 'vue';
import App from "@/App.vue";
import Notifications from '@kyvg/vue3-notification'
import router from "./Router.js"

Vue.createApp(App).use(router).use(Notifications).mount('#app');
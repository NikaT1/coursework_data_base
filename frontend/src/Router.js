import Index from "@/components/Index";
import Main from "@/components/Main";
import ProccessingAccusation from "@/components/Proccessing_accusation";
import NotFoundError from "@/components/Error";
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'index-page',
        component: Index
    },
    {
        path: '/auth',
        name: 'auth-page',
        component: Index
    },
    {
        path: '/main-inquisitor',
        name: 'main-inquisitor-page',
        component: Main,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                if (localStorage.getItem("role") == 0) {
                    next();
                }
                if (localStorage.getItem("role") == 1) {
                    next({ name: 'proccessing-acc-page' });
                }
            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/proccessing-acc',
        name: 'proccessing-acc-page',
        component: ProccessingAccusation,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                if (localStorage.getItem("role") == 0) {
                    next();
                }
                if (localStorage.getItem("role") == 1) {
                    next();
                }
            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'error-page',
        component: NotFoundError,
        props: {
            errorCode: "404",
            errorMessage: "Данной страницы не существует"
        }
    }
];


const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router;

import Index from "@/components/Index";
import Main from "@/components/Main";
import Proccessing from "@/components/Proccessing";
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
        beforeEnter: (to, from, next) =>
        {
//            if (localStorage.getItem("par") !== null) {
//                next()
//            } else next({name: 'auth-page'}); ------ чтобы тестировать без авторизации
            next()
        }
    },
    {
        path: '/proccessing-inq',
        name: 'proccessing-inq-page',
        component: Proccessing,
        beforeEnter: (to, from, next) => {
            //            if (localStorage.getItem("par") !== null) {
            //                next()
            //            } else next({name: 'auth-page'}); ------ чтобы тестировать без авторизации
            next()
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

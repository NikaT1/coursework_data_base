import Index from "@/components/Index";
import Main from "@/components/Main";
import SharePage from "@/components/Share_page";
import ProccessingAccusation from "@/components/Proccessing_accusation";
import ProccessingTorture from "@/components/Proccessing_torture";
import ProccessingDiscussion from "@/components/Proccessing_discussion";
import ProccessingPunishment from "@/components/Proccessing_punishment";
import ProccessingPreparingCases from "@/components/Proccessing_preparing_cases";
import ProccessingCases from "@/components/Proccessing_cases";
import AccusationRecord from "@/components/Accusation_record";
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
                } else {
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
                if (localStorage.getItem("role") != 0 && localStorage.getItem("inq_id") == 0) {
                    next({ name: 'share-page' });
                }
                if (localStorage.getItem("role") == 0 && localStorage.getItem("step") == 1) {
                    next();
                }
                if (localStorage.getItem("role") == 1 && localStorage.getItem("step") == 1) {
                    next();
                }
                if (localStorage.getItem("role") == 0 && localStorage.getItem("step") >= 2) {
                    next({ name: 'proccessing-cases' });
                }
                if (localStorage.getItem("role") == 1 && localStorage.getItem("step") >= 2) {
                    next({ name: 'proccessing-cases' });
                }
                if (localStorage.getItem("role") == 2) {
                    next({ name: 'proccessing-torture' });
                }
                if (localStorage.getItem("role") == 3) {
                    next({ name: 'proccessing-punishment' });
                }
                if (localStorage.getItem("role") == 4) {
                    next({ name: 'share-page' });
                }
            } else next({ name: 'auth-page' });
        } 
    },
    {
        path: '/proccessing-cases',
        name: 'proccessing-cases',
        component: ProccessingCases,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                if (localStorage.getItem("role") == 0 && localStorage.getItem("step") == 1) {
                    next({ name: 'auth-page' });
                }
                if (localStorage.getItem("role") == 1 && localStorage.getItem("step") == 1) {
                    next({ name: 'auth-page' });
                }
                if (localStorage.getItem("role") == 0 && localStorage.getItem("step") == 2) {
                    next();
                }
                if (localStorage.getItem("role") == 1 && localStorage.getItem("step") == 2) {
                    next();
                }
                if (localStorage.getItem("role") == 0 && localStorage.getItem("step") >= 3) {
                    next({ name: 'proccessing-preparing-cases' });
                }
                if (localStorage.getItem("role") == 1 && localStorage.getItem("step") >= 3) {
                    next({ name: 'proccessing-discussion' });
                }
                if (localStorage.getItem("role") == 2) {
                    next({ name: 'proccessing-torture' });
                }
            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/Proccessing-preparing-cases',
        name: 'proccessing-preparing-cases',
        component: ProccessingPreparingCases,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                if (localStorage.getItem("role") == 0) {
                    if (localStorage.getItem("step") == 3) {
                        next();
                    } else {
                        next({ name: 'main-inquisitor-page' });
                    }
                } else {
                    next({ name: 'auth-page' });
                }
                
            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/Proccessing-discussion',
        name: 'proccessing-discussion',
        component: ProccessingDiscussion,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                if (localStorage.getItem("role") == 1) {
                        next();
                } else {
                    next({ name: 'auth-page' });
                }

            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/Proccessing-torture',
        name: 'proccessing-torture',
        component: ProccessingTorture,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                if (localStorage.getItem("role") == 2) {
                        next();
                } else {
                    next({ name: 'auth-page' });
                }

            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/Proccessing-punishment',
        name: 'proccessing-punishment',
        component: ProccessingPunishment,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                next()

            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/share-page',
        name: 'share-page',
        component: SharePage,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                next()

            } else next({ name: 'auth-page' });
        }
    },
    {
        path: '/Accusation-record',
        name: 'accusation-record',
        component: AccusationRecord,
        beforeEnter: (to, from, next) => {
            if (localStorage.getItem("token") !== null) {
                next()

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

<template>

    <div class="main-background" id="main-div">
        <Header />
        <div class="div-block">
            <TextBlock v-if="info" v-on:click="start($event)" button_msg="Начать">
                Данное веб-приложение представляет бизнес-процессы испанской инквизиции. <br><br>
                Роль Инквизитор позволяет управлять инквизиционным процессом, сбором доносов, формированием и ведением дел.<br>
                Роль Епископ позволяет фиксировать доносы и проводить беседы в церкви. <br>
                Роль Фискал позволяет проводить пыточный процесс.
            </TextBlock>
            <AccountBlock v-if="account" v-model:login="login" v-model:password="password"
                          v-on:createUser="createUser($event)"
                          v-on:logIn="logIn($event)" />
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import TextBlock from "@/components/pcomponents/blocks/TextBlock";
    import AccountBlock from "@/components/pcomponents/blocks/AccountBlock";
    import Footer from "@/components/pcomponents/blocks/Footer";
    import { mapState } from 'vuex';

    export default {
        components: {
            Footer,
            Header,
            TextBlock,
            AccountBlock,
        },
        name: "Index",
        data() {
            return {
                login: "",
                password: "",
                account: false,
                info: true,
            }
        },
        beforeMount() {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
        },

        computed: mapState({
            token: state => state.accounts.token,
            role: state => state.accounts.role,
            name: state => state.inquisition.person_name,
        }),
        methods: {
            createUser() {
                const login = this.login;
                const password = this.password;
                /*this.$store.dispatch('CREATE_NEW_ACCOUNT', { login, password })
                    .then(() => {
                        localStorage.setItem("token", token);
                        localStorage.setItem("role", role);
                        this.$store.dispatch('INITIAL_ACT');
                        this.$router.push({ name: 'main-inquisitor-page' });
                    })
                    .catch(err => this.showError(err));*/
                
                this.$store.dispatch('CREATE_NEW_ACCOUNT', { login, password });
                this.$store.dispatch('INITIAL_ACT');
        
                localStorage.setItem("token", this.token);
                localStorage.setItem("role", this.role);
                this.$router.push({ name: 'main-inquisitor-page' });
            },
            logIn() {
                const login = this.login;
                const password = this.password;
                /*this.$store.dispatch('CREATE_NEW_ACCOUNT', { login, password })
                    .then(() => {
                        localStorage.setItem("token", token);
                        localStorage.setItem("role", role);
                        this.$store.dispatch('INITIAL_ACT');
                        this.$router.push({ name: 'main-inquisitor-page' });
                    })
                    .catch(err => this.showError(err));*/
                this.$store.dispatch('LOG_IN_ACCOUNT', { login, password });
                this.$store.dispatch('INITIAL_ACT');
                localStorage.setItem("token", this.token);
                localStorage.setItem("role", this.role);
                this.$router.push({ name: 'main-inquisitor-page' });
            },
            start() {
                this.account = true
                this.info = false
            },
        }
    }
</script>

<style scoped>

    #main-div {
        min-width: 100%;
        min-height: 100%;
        position: relative;
    }

    .div-block {
        display: block;
        margin: 6% 0 0 0;
    }
</style>
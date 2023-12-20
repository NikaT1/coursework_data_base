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
            <AccountBlock v-if="account" />
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import TextBlock from "@/components/pcomponents/blocks/TextBlock";
    import AccountBlock from "@/components/pcomponents/blocks/AccountBlock";
    import Footer from "@/components/pcomponents/blocks/Footer";

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
                account: false,
                info: true,
            }
        },
        beforeMount() {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            localStorage.removeItem('step');
        },


        methods: {
            start() {
                this.account = true
                this.info = false
            },
            showError(err) {
                console.log(err );
                let text = "Произошла непредвиденная ошибка";
                if (err.code == 500 || err.response.status == 500) {
                    text = "Проблема с подключением к серверу";
                }
                if (err.code == 404 || err.response.status == 404) {
                    text = "Неверный запрос к серверу";
                }
                if (err.code == 401 || err.response.status == 401) {
                    text = "Данного аккаунта не существует";
                }
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: text,
                    type: 'error'
                });
            }
        }
    }
</script>

<style scoped>

    #main-div {
        min-width: 100%;
        box-sizing: border-box;
        min-height: calc(100vh - 80px);
        padding-bottom: 90px;
        position: relative;
    }

    .div-block {
        display: block;
        margin: 6% 0 0 0;
    }
</style>
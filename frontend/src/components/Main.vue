<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div class="div-block" id="div-inline">
                <div v-if="new_inq" class="div-block table-name">
                    Создание нового инквизиционного процесса
                </div>
                <div v-if="main_info" class="div-block table-name">
                    Возможные действия для Инквизитора
                </div>
                <ArgsBlockInq v-if="new_inq" class="div-block" v-model:p_locality="p_locality" v-model:p_bible="p_bible" />
                <div v-if="new_inq" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="new_inq_buttons" v-on:goBackToMain="goBackToMain" v-on:createNew="createNew" />
                </div>
                <div v-if="main_info" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="start_buttons" v-on:goBack="goBack" v-on:startNew="startNew" v-on:openCurrent="openCurrent" />
                </div>
            </div>
            <div class="div-block table-name">
                Список прошлых инквизиционных процессов:
            </div>
        </div>
        <div class="div-block" id="result-table">
            <DataTable :value="data" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem">
                <Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header" style="width: 24%"></Column>
            </DataTable>
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
    import Footer from "@/components/pcomponents/blocks/Footer";
    import ArgsBlockInq from "@/components/pcomponents/blocks/ArgsBlockInq";
    import { mapState } from 'vuex';
    import DataTable from 'primevue/datatable';
    import Column from 'primevue/column';
    export default {
        components: {
            Footer,
            Header,
            ButtonsBlock,
            ArgsBlockInq,
            DataTable,
            Column,
        },
        name: 'Main',
        data() {
            return {
                start_buttons: [
                    { msg: 'выйти', command: 'goBack' },
                    { msg: 'новый инквизиционный процесс', command: 'startNew' },
                    { msg: 'текущий инквизиционный процесс', command: 'openCurrent' }
                ],
                new_inq_buttons: [
                    { msg: 'создать', command: 'createNew' },
                    { msg: 'назад', command: 'goBackToMain' }
                ],
                new_inq: false,
                main_info: true,
                p_bible: null,
                p_locality: null,
                columns: [
                    { field: 'startTime', header: 'Дата начала' },
                    { field: 'locality', header: 'Местность' },
                    { field: 'inquisitor', header: 'Инквизитор' },
                    { field: 'caseCount', header: 'Кол-во дел' },
                    { field: 'endTime', header: 'Дата окончания' },
                ],
            }
        },
        created() {
            this.$store.dispatch('GET_ALL_INQUISITIONS');
        },
        computed: mapState({
            data: state => state.inquisition.inq_table_data
        }),
        methods: {
            handleClose() {
                localStorage.removeItem("token");
            },
            goBackToMain() {
                this.new_inq = false;
                this.main_info = true;
            },
            goBack() {
                localStorage.removeItem("token");
                this.$router.push({ name: 'auth-page' });
            },
            startNew() {
                this.new_inq = true;
                this.main_info = false;
            },
            createNew() {
                console.log(this.p_locality, this.p_bible);
                let localityId = this.p_locality.id;
                let bibleId = this.p_bible.version;
                this.$store.dispatch('CREATE_NEW_INQ', { localityId, bibleId })
                    .then(resp => {
                        console.log(resp);
                        this.$store.dispatch('START_ACCUSATION_PROCESS');
                        console.log(localStorage.getItem('step'));
                        this.$router.push({ name: 'proccessing-acc-page' });
                    },
                        err => (this.showError(err)));
            },
            openCurrent() {
                this.$store.dispatch('GET_CUR_INQ')
                    .then(resp => {
                        console.log(resp);
                        this.$router.push({ name: 'proccessing-acc-page' });
                    },
                        err => (this.showError(err)));
            },
            showError(err) {
                console.log(err);
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
        },
    }
</script>
<style>

    .table-name {
        font-size: medium;
        color: #6d747f;
        font-size: 20px;
        padding: 20px;
        font-weight: bold;
    }

    #div-inline div {
        vertical-align: middle;
        margin: 20px 20px 20px;
        text-align: center;
    }

    .main-background > div:first-child {
        min-height: calc(100vh - 80px);
        display: table;
        margin: 0 auto;
    }

    #result-table {
        overflow-x: auto;
        height: 300px;
        margin: 10px 20px;
    }

    .div-block {
        display: block;
    }

    .div-inline {
        display: inline-block;
    }

    #div-buttons {
        padding: 1.5% 1.5% 1.5% 1.5%;
    }

    @media (max-width: 1228px) {
        #div-inline div {
            margin: 10px 10px 10px;
        }
    }

    @media (max-width: 892px) {
        #div-inline div {
            margin: 5px 5px 5px;
        }
    }
</style>
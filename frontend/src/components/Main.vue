<template>
    <div id="main-div">
        <Header />
        <div class="main-background">
            <div class="background">
                <div v-if="new_inq" class="table-name">
                    Создание нового инквизиционного процесса
                    <ArgsBlockInq v-if="new_inq" class="div-block" v-model:p_locality="p_locality" v-model:p_bible="p_bible" />

                </div>
                <div v-if="main_info" class="table-name div-block">
                    Возможные действия для Инквизитора
                    <ArgsBlockInq v-if="new_inq" class="div-block" v-model:p_locality="p_locality" v-model:p_bible="p_bible" />

                </div>
                <div v-if="new_inq">
                    <ButtonsBlock v-bind:buttons="new_inq_buttons" v-on:goBackToMain="goBackToMain" v-on:createNew="createNew" />
                </div>
                <div v-if="main_info">
                    <ButtonsBlock v-bind:buttons="start_buttons" v-on:goBack="goBack" v-on:startNew="startNew" v-on:openCurrent="openCurrent" />
                </div>
            </div>
            <div class="div-block table-name">
                Список прошлых инквизиционных процессов:
            </div>
        </div>
        <div>
            <DataTable :value="data" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem">
                <Column v-for="col of columns" :key="col.field" :field="col.field" sortable :header="col.header" style="width: 24%"></Column>
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
                    { msg: 'назад', command: 'goBackToMain' },
                    { msg: 'создать', command: 'createNew' },
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
            data: state => state.inquisition.inq_table_data,
            cur_inq: state => state.cur_inq
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
                if (this.check_new_inq()) {
                    console.log(this.p_locality, this.p_bible);
                    let localityId = this.p_locality.id;
                    let bibleId = this.p_bible.version;
                    this.$store.dispatch('CREATE_NEW_INQ', { localityId, bibleId })
                        .then(resp => {
                            console.log(resp);
                            this.$store.dispatch('START_ACCUSATION_PROCESS')
                                .then(() => this.$router.push({ name: 'proccessing-acc-page' }));
                        },
                            err => (this.showError(err)));
                } else {
                    this.showErrorFromFront("Необходимо заполнить все поля!");
                }
            },
            openCurrent() {
                this.$store.dispatch('GET_CUR_INQ')
                    .then(resp => {
                        console.log(resp);
                        if (localStorage.getItem("inq_id") == 0) {
                            this.showInfo("Текущая инквизиция не найдена");
                        } else {
                            this.$router.push({ name: 'proccessing-acc-page' });
                        }
                    },
                        err => (this.showError(err)));
            },
            check_new_inq() {
                return this.p_locality != null && this.p_locality != undefined && this.p_bible != null && this.p_bible != undefined;
            },

            showErrorFromFront(text) {
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: text,
                    type: 'error'
                });
            },
            showError(err) {
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: err.message,
                    type: 'error'
                });
            },
            showInfo(msg) {
                this.$notify({
                    group: "info",
                    title: 'Внимание!',
                    text: msg,
                    type: 'info'
                });
            }
        },
    }
</script>
<style>
    .background {
        margin: 0 auto;
        padding: 5px 5px 5px 5px;
        width: 60%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .background div {
        
        display: inline-block;
    }


    .main-background {
        
    }

    .title {
        text-align: center;
    }


    .table-name {
        color: #6d747f;
        font-size: 15px;
        padding: 5px;
        font-weight: bold;
    }

    #main-div {
        min-width: 100%;
        box-sizing: border-box;
        min-height: calc(100vh - 50px);
        position: relative;
        padding-bottom: 60px;
    }

    #div-inline {
        width: 100%;
    }

    .div-block {
        justify-content: center;
        display: flex;
        margin: 0 auto;
    }
</style>
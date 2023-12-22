<template>
    <div id="div-main">
        <Header />
        <div class="main-background">
            <div v-if="main_inf" class="table-name">
                Идет процесс сбора доносов
            </div>
            <div v-if="new_rec" class="table-name">
                Создание нового доноса
            </div>
            <div id="div-inline">
                <ArgsBlockRecord v-if="new_rec" v-model:p_accused="p_accused" v-model:p_informer="p_informer" v-model:p_cur_violation_place="p_cur_violation_place" v-model:p_cur_date_time="p_cur_date_time" v-model:p_cur_description="p_cur_description" />
                <div v-if="is_inq && main_inf">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:newAcc="newAcc" v-on:finishAcc="finishAcc" />
                </div>
                <div v-if="is_bish && main_inf">
                    <ButtonsBlock v-bind:buttons="buttons_for_bish" v-on:goBack="goBack" v-on:newAcc="newAcc" />
                </div>
                <div v-if="new_rec">
                    <ButtonsBlock v-bind:buttons="buttons_for_new_rec" v-on:goBackToMain="goBackToMain" v-on:createNewAcc="createNewAcc" />
                </div>
            </div>
            <div class="table-name">
                Список доносов:
            </div>
        </div>
        <div class="card">
            <DataTable :value="data" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="min-width: 50rem">
                <Column v-for="col of columns" :key="col.field" :field="col.field" sortable :header="col.header" style="width: 20%"></Column>
            </DataTable>
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
    import ArgsBlockRecord from "@/components/pcomponents/blocks/ArgsBlockRecord";
    import Footer from "@/components/pcomponents/blocks/Footer";
    import { mapState } from 'vuex';
    import DataTable from 'primevue/datatable';
    import Column from 'primevue/column';

    export default {
        components: {
            Footer,
            Header,
            ButtonsBlock,
            DataTable,
            ArgsBlockRecord,
            Column,
        },
        name: 'Proccessing_accusation',
        data() {
            return {
                data: null,
                main_inf: true,
                new_rec: false,
                buttons_for_inq: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'новый донос', command: 'newAcc' },
                    { msg: 'закончить сбор доносов', command: 'finishAcc' },
                ],
                buttons_for_bish: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'новый донос', command: 'newAcc' },
                ],
                buttons_for_new_rec: [
                    { msg: 'назад', command: 'goBackToMain' },
                    { msg: 'создать', command: 'createNewAcc' },
                ],
                is_inq: (localStorage.getItem("role") == '0'),
                is_bish: (localStorage.getItem("role") == '1'),
                columns: [
                    { field: 'informer', header: 'Доносчик' },
                    { field: 'bishop', header: 'Епископ' },
                    { field: 'accused', header: 'Обвиненный' },
                    { field: 'violationPlace', header: 'Место преступления' },
                    { field: 'dateTime', header: 'Дата' },
                    { field: 'description', header: 'Описание' },
                ],
                p_accused: null,
                p_informer: null,
                p_cur_violation_place: "",
                p_cur_date_time: "",
                p_cur_description: "",
            }
        },
        computed: mapState({
            cur_data: state => state.inquisition.acc_table_data
        }),
        methods: {
            handleClose() {
                localStorage.removeItem("token");
            },
            goBack() {
                if (localStorage.getItem("role") == 0) {
                    this.$router.push({ name: 'main-inquisitor-page' });
                } else {
                    this.$router.push({ name: 'auth-page' });
                }
            },
            newAcc() {
                this.main_inf = false;
                this.new_rec = true;
            },
            goBackToMain() {
                this.main_inf = true;
                this.new_rec = false;
            },
            finishAcc() {
                this.$store.dispatch('FINISH_ACCUSATION_PROCESS')
                    .then(() => this.$router.push({ name: 'proccessing-cases' }));
            },
            createNewAcc() {
                if (this.check_new_acc()) {
                    let accused = this.p_accused.id;
                    let informer = this.p_informer.id;
                    let violationPlace = this.p_cur_violation_place;
                    let dateTime = this.getStringDate(this.p_cur_date_time);
                    let description = this.p_cur_description;
                    console.log(accused, informer, violationPlace, dateTime, description);
                    this.$store.dispatch('ADD_ACC_RECORD', { accused, informer, violationPlace, dateTime, description })
                        .then((resp) => {
                            console.log(resp);
                            this.main_inf = true;
                            this.new_rec = false;
                            this.$store.dispatch('GET_ALL_ACCUSATION_RECORDS')
                                .then(() => this.data = this.cur_data);
                            
                        },
                            err => this.showError(err));
                } else {
                    this.showErrorFromFront("Необходимо заполнить все поля!");
                }
            },
            getStringDate(date) {
                let str_date = date.getFullYear() + "-";
                if (date.getMonth() < 10) {
                    str_date = str_date + "0" + (date.getMonth() + 1) + "-";
                } else {
                    str_date = str_date + (date.getMonth() + 1) + "-";
                }
                if (date.getDate() < 10) {
                    str_date = str_date + "0" + date.getDate();
                } else {
                    str_date = str_date + date.getDate();
                }
                return str_date;
            },
            check_new_acc() {
                return this.p_accused != null && this.p_accused != undefined && this.p_informer != null && this.p_informer != undefined &&
                    this.p_cur_violation_place != "" && this.p_cur_date_time != undefined && this.p_cur_date_time != null && this.p_cur_description != "";
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
        created() {
            this.$store.dispatch('GET_ALL_ACCUSATION_RECORDS')
                .then(() => this.data = this.cur_data);
           
        }
    }
</script>
<style>
    #div-inline {
        width: 100%;
        justify-content: center;
    }

    #main-div {
        min-width: 100%;
        box-sizing: border-box;
        min-height: calc(100vh - 80px);
        padding-bottom: 90px;
        position: relative;
    }
</style>
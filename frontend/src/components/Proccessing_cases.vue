<template>
    <div>
        <Header />
        <div class="main-background">
            <div v-if="main_inf" class="table-name">
                Идет процесс обработки доносов
            </div>
            <div v-if="new_rec" class="table-name">
                Привязка сводов к доносу
            </div>
            <div class="background" id="div-inline">
              
                <ArgsBlockCase v-if="new_rec" class="div-block" v-model:p_commandments="p_commandments" />
                <div v-if="is_inq && main_inf">
                    <div>Для привязки доноса к сводам кликните в таблице на нужный донос и нажмите "утвердить донос" </div>
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:connectAcc="connectAcc" v-on:startGeneratingCases="startGeneratingCases" />
                </div>
                <div v-if="is_bish && main_inf">
                    <div>Для привязки доноса к сводам кликните в таблице на нужный донос и нажмите "утвердить донос" </div>
                    <ButtonsBlock v-bind:buttons="buttons_for_bish" v-on:goBack="goBack" v-on:connectAcc="connectAcc" />
                </div>
                <div v-if="new_rec">
                    <ButtonsBlock v-bind:buttons="buttons_for_connect" v-on:goBackToMain="goBackToMain" v-on:doConnect="doConnect" />
                </div>
            </div>
            <div class="div-block table-name">
                Список необработанных доносов:
            </div>
        </div>
        <div class="card">
            <DataTable v-model:selection="selectedData" :value="data" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" selectionMode="single" dataKey="id" tableStyle="min-width: 50rem">
                <Column v-for="col of columns" :key="col.field" :field="col.field" sortable :header="col.header" style="width: 20%"></Column>
            </DataTable>
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
    import ArgsBlockCase from "@/components/pcomponents/blocks/ArgsBlockCase";
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
            ArgsBlockCase,
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
                    { msg: 'утвердить донос', command: 'connectAcc' },
                    { msg: 'закончить формирование дел', command: 'startGeneratingCases' },
                ],
                buttons_for_bish: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'утвердить донос', command: 'connectAcc' },
                ],
                buttons_for_connect: [
                    { msg: 'назад', command: 'goBackToMain' },
                    { msg: 'утвердить', command: 'doConnect' },
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
                selectedData: null,
                p_commandments: null,
            }
        },
        computed: mapState({
            cur_data: state => state.inquisition.acc_nr_table_data
        }),
        watch: {
            selectedData(val) {
                console.log(val);
            }
        },
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
            connectAcc() {
                if (this.selectedData != null && this.selectedData != undefined) {
                    this.main_inf = false;
                    this.new_rec = true;
                } else {
                    console.log("here");
                    this.showErrorFromFront("Необходимо выбрать донос!");
                }
            },
            goBackToMain() {
                this.main_inf = true;
                this.new_rec = false;
            },
            startGeneratingCases() {
                this.$store.dispatch('FINISH_RESOLVING_RECORDS')
                    .then(() => this.$router.push({ name: 'proccessing-preparing-cases' }));
               
            },
            doConnect() {
                if (this.check_new_connect()) {
                    let commandments = this.p_commandments.map(item => item.id);
                    let record_id = this.selectedData.id;
                    console.log(commandments, record_id);
                    this.$store.dispatch('CONNECT_COMMANDMENT', { commandments, record_id })
                        .then((resp) => {
                            console.log(resp);
                            this.$store.dispatch('GET_NR_ACCUSATION_RECORDS')
                                .then(() => this.data = this.cur_data);
                            this.main_inf = true;
                            this.new_rec = false;
                        },
                            err => this.showError(err));
                } else {
                    this.showErrorFromFront("Необходимо выбрать хотя бы один свод!");
                }

            },
            check_new_connect() {
                return this.p_commandments != null && this.p_commandments != undefined && this.selectedData != null && this.selectedData != undefined;
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
            this.$store.dispatch('GET_NR_ACCUSATION_RECORDS')
                .then(() => this.data = this.cur_data);
           
        }
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

</style>
<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div v-if="main_inf" class="div-block table-name">
                Идет процесс обработки доносов
            </div>
            <div v-if="new_rec" class="div-block table-name">
                Привязка сводов к доносу
            </div>
            <div v-if="main_inf" class="div-block table-name">
                Для привязки доноса к сводам кликните в таблице на нужный донос и нажмите "утвердить донос"
            </div>
            <div class="div-block" id="div-inline">
                <ArgsBlockCase v-if="new_rec" class="div-block" v-model:p_commandments="p_commandments" />
                <div v-if="is_inq && main_inf" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:connectAcc="connectAcc" v-on:startGeneratingCases="startGeneratingCases" />
                </div>
                <div v-if="is_bish && main_inf" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_bish" v-on:goBack="goBack" v-on:connectAcc="connectAcc" />
                </div>
                <div v-if="new_rec" class="div-inline" id="div-buttons">
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
                    { field: 'violation_place', header: 'Место преступления' },
                    { field: 'date_time', header: 'Дата' },
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
                if (this.selectedData !== null && this.selectedData !== undefined ) {
                    this.main_inf = false;
                    this.new_rec = true;
                } else {
                    console.log("here");
                    this.showError("Необходимо выбрать донос!");
                }
            },
            goBackToMain() {
                this.main_inf = true;
                this.new_rec = false;
            },
            startGeneratingCases() {
                this.$store.dispatch('FINISH_RESOLVING_RECORDS');
                this.$router.push({ name: 'proccessing-preparing-cases' });
            },
            doConnect() {
                let commandments_id = this.p_commandments.map(item => item.id);
                let record_id = this.selectedData.id;
                console.log(commandments_id, record_id);
                //this.$store.dispatch('CONNECT_COMMANDMENT', {commandments_id, record_id})
                //    .then(() => {
                //          this.$store.dispatch('GET_NR_ACCUSATION_RECORDS');
                //          this.data = this.cur_data;
                //          this.main_inf = true;
                //          this.new_rec = false;
                //        }))
                //    .catch(err => this.showError(err));
                this.$store.dispatch('CONNECT_COMMANDMENT', { commandments_id, record_id });
                this.$store.dispatch('GET_NR_ACCUSATION_RECORDS');
                this.main_inf = true;
                this.new_rec = false;
                this.data = this.cur_data;
                console.log(this.data);
            },
            showError(text) {
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: text,
                    type: 'error'
                });
            }
        },
        created() {
            this.$store.dispatch('GET_NR_ACCUSATION_RECORDS');
            this.data = this.cur_data;
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

    #div-inline div {
        vertical-align: middle;
        margin: 20px 20px 20px;
        text-align: center;
    }

    .main-background > div:first-child {
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
<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div v-if="closed == false" class="div-block table-name">
                Идет процесс разрешения дел
            </div>
            <div v-if="closed == true" class="div-block table-name">
                Инквизиционный процесс окончен
            </div>
            <div v-if="closed == false" class="div-block table-name">
                Выберите дело (кликнув по нужной строке в таблице) и нажмите на кнопку нужной команды
            </div>
            <div class="div-block" id="div-inline">
                <div v-if="closed == false" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:doNextStep="doNextStep" />
                </div>
                <div v-if="closed == true" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:doNextStep="doNextStep" />
                </div>
            </div>
            <div v-if="closed == false" class="div-block table-name">
                Список дел:
            </div>
            <div v-if="closed == true" class="div-block table-name">
                Итоги:
            </div>
        </div>
        <div class="card" v-if="closed == false">
            <DataTable v-model:selection="selectedData" :value="data" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" selectionMode="single" dataKey="id" tableStyle="min-width: 50rem">
                <Column v-for="col of columns" :key="col.field" :field="col.field" sortable :header="col.header" style="width: 20%"></Column>
            </DataTable>
        </div>
        <div class="card" v-if="closed == true">
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
            Column,
        },
        name: 'ProccessingPreparingCases',
        data() {
            return {
                closed: false,
                data: null,
                buttons_for_inq: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'отправить на следующий этап', command: 'doNextStep' },
                ],
                columns: [
                    { field: 'creation_date', header: 'Дата создания' },
                    { field: 'accused', header: 'Обвиненный' },
                    { field: 'violation_description', header: 'Своды' },
                    { field: 'description', header: 'Описание' },
                    { field: 'status', header: 'Статус' },
                ],
                selectedData: null,
            }
        },
        computed: mapState({
            cur_data: state => state.inquisition.cases_data,
        }),
        watch: {
            data(val) {
                if (val.length == 0) {
                    this.closed = true;
                }
            },
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
            doNextStep() {
                if (this.selectedData !== null && this.selectedData !== undefined ) {
                    let case_id = this.selectedData.id;
                    console.log(case_id);
                    if (this.selectedData.step == 0) {
                        //this.$store.dispatch('SEND_TO_DISCUSSION', {case_id})
                        //    .then(() => {
                        //          this.$store.dispatch('GET_ALL_CASES');
                        //          this.data = this.cur_data;
                        //          this.main_inf = true;
                        //          this.new_rec = false;
                        //        }))
                        //    .catch(err => this.showError(err));
                        this.$store.dispatch('SEND_TO_DISCUSSION', { case_id });
                        this.$store.dispatch('GET_ALL_CASES');
                        this.data = this.cur_data;
                        console.log(this.data);
                    } else if (this.selectedData.step == 2) {
                        //this.$store.dispatch('SEND_TO_TORTURE', {case_id})
                        //    .then(() => {
                        //          this.$store.dispatch('GET_ALL_CASES');
                        //          this.data = this.cur_data;
                        //          this.main_inf = true;
                        //          this.new_rec = false;
                        //        }))
                        //    .catch(err => this.showError(err));
                        this.$store.dispatch('SEND_TO_TORTURE', { case_id });
                        this.$store.dispatch('GET_ALL_CASES');
                        this.data = this.cur_data;
                        console.log(this.data);
                    } else {
                        this.showError("Данное дело нельзя выбрать, так как текущий процесс еще не окончен!");
                    }
                    
                } else {
                    this.showError("Необходимо выбрать дело!");
                }
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
            this.$store.dispatch('GET_ALL_CASES');
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
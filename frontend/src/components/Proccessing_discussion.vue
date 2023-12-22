<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div v-if="main_inf" class="div-block table-name">
                Процесс проведения беседы
            </div>
            <div v-if="is_empty" class="div-block table-name">
                Очередь на беседу пока что пуста!
            </div>
            <div v-if="new_rec" class="div-block table-name">
                Добавление результата
            </div>
            <div v-if="main_inf" class="div-block table-name">
                Для проведения беседы кликните в таблице на нужное дело и нажмите "провести беседу"
            </div>
            <div class="div-block" id="div-inline">
                <ArgsBlockDiscussion v-if="new_rec" class="div-block" v-model:p_discription="p_discription" v-model:p_result="p_result" />
                <div v-if="main_inf" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:connectAcc="startDis" />
                </div>
                <div v-if="new_rec" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_connect" v-on:goBackToMain="goBackToMain" v-on:doConnect="finishDis" />
                </div>
            </div>
            <div class="div-block table-name">
                Очередь дел на беседу:
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
    import ArgsBlockDiscussion from "@/components/pcomponents/blocks/ArgsBlockDiscussion";
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
            ArgsBlockDiscussion,
            Column,
        },
        name: 'Proccessing_discussion',
        data() {
            return {
                data: null,
                main_inf: true,
                new_rec: false,
                buttons_for_inq: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'провести беседу', command: 'startDis' },
                ],
                buttons_for_connect: [
                    { msg: 'назад', command: 'goBackToMain' },
                    { msg: 'закончить беседу', command: 'finishDis' },
                ],
                columns: [
                    { field: 'informer', header: 'Доносчик' },
                    { field: 'bishop', header: 'Епископ' },
                    { field: 'accused', header: 'Обвиненный' },
                    { field: 'violation_place', header: 'Место преступления' },
                    { field: 'date_time', header: 'Дата' },
                    { field: 'description', header: 'Описание' },
                ],
                selectedData: null,
                p_result: null,
                p_description: "",
                is_empty: false,
            }
        },
        computed: mapState({
            cur_data: state => state.inquisition.queue_for_disscution,
        }),
        watch: {
            data(val) {
                if (val.length == 0) {
                    this.is_empty = true;
                } else {
                    this.is_empty = false;
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
            startDis() {
                if (this.selectedData != null && this.selectedData != undefined) {
                    this.main_inf = false;
                    this.new_rec = true;
                } else {
                    this.showErrorFromFront("Необходимо выбрать дело!");
                }
            },
            goBackToMain() {
                this.main_inf = true;
                this.new_rec = false;
            },
            finishDis() {
                if (this.check_new_dis()) {
                    let resultId = this.p_result.id;
                    let description = this.p_description;
                    let id = this.selectedData.id;

                    this.$store.dispatch('FINISH_DISCUSSION', { resultId, description, id })
                        .then((resp) => {
                            console.log(resp);
                            this.$store.dispatch('GET_QUEUE_FOR_DISCUTTION')
                                .then(() => this.data = this.cur_data);
                            this.main_inf = true;
                            this.new_rec = false;
                        },
                            err => this.showError(err));
                } else {
                    this.showErrorFromFront("Необходимо заполнить все поля!");
                }

            },
            check_new_dis() {
                return this.p_result != null && this.p_result != undefined && this.selectedData != null && this.selectedData != undefined &&
                    this.p_description != "";
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
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: err.message,
                    type: 'error'
                });
            }
        },
        created() {
            this.$store.dispatch('GET_QUEUE_FOR_DISCUTTION')
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
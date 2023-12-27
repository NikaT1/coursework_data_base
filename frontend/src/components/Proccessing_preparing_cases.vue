<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div v-if="closed == false" class="table-name">
                Идет процесс разрешения дел
            </div>
            <div v-if="closed == true" class="table-name">
                Инквизиционный процесс окончен
            </div>
            <div class="background" id="div-inline">
                <div v-if="closed == false">
                    <div>
                        Выберите дело (кликнув по нужной строке в таблице) и нажмите на "отправить на следующий этап"
                    </div>
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:doNextStep="doNextStep" />
                </div>
                <div v-if="closed == true">
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
                <Column v-for="col of columns" :key="col.field" :field="col.field" sortable :header="col.header" style="width: 25%"></Column>
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
                    { field: 'creationDate', header: 'Дата создания' },
                    { field: 'accused', header: 'Обвиненный' },
                    { field: 'violationDescription', header: 'Своды' },
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
                    this.$store.dispatch('FINISH_INQUISITION_PROCESS')
                        .then((resp) => {
                            console.log(resp);
                            this.$router.push({ name: 'proccessing-punishment' });
                        },
                            err => this.showError(err));
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
                if (this.selectedData !== null && this.selectedData !== undefined) {
                    let id = this.selectedData.id;
                    console.log(id);
                    if (this.selectedData.step == 0) {
                        this.$store.dispatch('SEND_TO_DISCUSSION', { id })
                            .then((resp) => {
                                console.log(resp);
                                this.$store.dispatch('GET_ALL_CASES')
                                    .then(() => {
                                        this.data = this.cur_data;
                                        this.main_inf = true;
                                        this.new_rec = false;
                                    });

                            },
                                err => this.showError(err));

                    } else if (this.selectedData.step == 2) {
                        this.$store.dispatch('SEND_TO_TORTURE', { id })
                            .then((resp) => {
                                console.log(resp);
                                this.$store.dispatch('GET_ALL_CASES')
                                    .then(() => {
                                        this.data = this.cur_data;
                                        this.main_inf = true;
                                        this.new_rec = false;
                                    });
                            },
                                err => this.showError(err));

                    } else {
                        this.showErrorFromFront("Данное дело нельзя выбрать, так как текущий процесс еще не окончен!");
                    }

                } else {
                    this.showErrorFromFront("Необходимо выбрать дело!");
                }
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
            this.$store.dispatch('GET_ALL_CASES')
                .then(() => this.data = this.cur_data);

        }
    }
</script>
<style>
</style>
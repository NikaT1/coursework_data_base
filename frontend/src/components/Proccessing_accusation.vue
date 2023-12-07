<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div v-if="main_inf" class="div-block table-name">
                Идет процесс сбора доносов
            </div>
            <div v-if="new_rec" class="div-block table-name">
                Создание нового доноса
            </div>
            <div class="div-block" id="div-inline">
                <ArgsBlockRecord v-if="new_rec" class="div-block" v-model:p_accused="p_accused" v-model:p_informer="p_informer" v-model:p_cur_violation_place="p_cur_violation_place" v-model:p_cur_date_time="p_cur_date_time" v-model:p_cur_description="p_cur_description" />
                <div v-if="is_inq && main_inf" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:newAcc="newAcc" v-on:finishAcc="finishAcc" />
                </div>
                <div v-if="is_bish && main_inf" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_bish" v-on:goBack="goBack" v-on:newAcc="newAcc" />
                </div>
                <div v-if="new_rec" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_new_rec" v-on:goBackToMain="goBackToMain" v-on:createNewAcc="createNewAcc" />
                </div>
            </div>
            <div class="div-block table-name">
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
                    { field: 'violation_place', header: 'Место преступления' },
                    { field: 'date_time', header: 'Дата' },
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
                this.$router.push({ name: 'proccessing-cases' });
            },
            createNewAcc() {
                let accused = this.p_accused;
                let informer = this.p_informer;
                let violation_place = this.p_cur_violation_place;
                let date_time = this.p_cur_date_time;
                let description = this.p_cur_description;
                console.log(accused, informer, violation_place, date_time, description);
                //this.$store.dispatch('ADD_ACC_RECORD', { accused, informer, violation_place, date_time, description})
                //    .then(() => {
                //          this.main_inf = true;
                //          this.new_rec = false;
                //        }))
                //    .catch(err => this.showError(err));
                this.$store.dispatch('ADD_ACC_RECORD', { accused, informer, violation_place, date_time, description });
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
            this.$store.dispatch('GET_ALL_ACCUSATION_RECORDS');
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
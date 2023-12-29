<template>
    <div id="main-div">
        <Header />
        <div class="main-background">
            <div v-if="main_inf" class="table-name">
                Результаты обработки дел - назначенные наказания 
            </div>
            <div id="div-inline">
                <div v-if="main_inf">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:connectAcc="startDis" />
                </div>
      
            </div>
            <div class="table-name">
                Назначенные наказания:
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
        name: 'Proccessing_punishment',
        data() {
            return {
                data: null,
                main_inf: true,
                buttons_for_inq: [
                    { msg: 'назад', command: 'goBack' },
                ], 
       
                columns: [
                    { field: 'accused', header: 'Обвиненный' },
                    { field: 'punishment', header: 'Наказание' },
                    { field: 'prisonName', header: 'Тюрьма' },
                    { field: 'violationDescription', header: 'Описание преступления' },
                    { field: 'creationDate', header: 'Дата' },
                    { field: 'description', header: 'Описание' },
                ],
        
            }
        },
        computed: mapState({
            cur_data: state => state.inquisition.queue_for_punishment,
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
            this.$store.dispatch('GET_QUEUE_FOR_PUNISHMENT')
                .then((resp) => {
                    console.log(resp);
                    this.data = this.cur_data;
                },
                    err => this.showError(err));
        }
    }
</script>
<style>

</style>
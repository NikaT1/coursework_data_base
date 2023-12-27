<template>
    <div>
        <Header />
        <div class="main-background">
            <div class="table-name">
                В данный момент в вашей местности не идет инквизиция
            </div>

            <div class="div-block table-name">
                Список сводов в библии:
            </div>

        </div>
        <div class="card">
            <DataTable :value="commandments_data" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" dataKey="id" tableStyle="min-width: 50rem">
                <Column v-for="col of columns" :key="col.field" :field="col.field" sortable :header="col.header" style="width: 20%"></Column>
            </DataTable>
            <div class="background">
                <ButtonsBlock v-bind:buttons="buttons" v-on:goBack="goBack" />
                <div>Выберите библию:</div>
                <Dropdown v-model="bible" :options="bible_data" filter optionLabel="name" class="w-full md:w-14rem" />

            </div>
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
    import Dropdown from 'primevue/dropdown';

    export default {
        components: {
            Footer,
            Header,
            ButtonsBlock,
            DataTable,
            Column,
            Dropdown,
        },
        name: 'SharePage',
        data() {
            return {

                buttons: [
                    { msg: 'назад', command: 'goBack' },
                ],

                columns: [
                    { field: 'description', header: 'Описание свода' },

                ],
                bible: null,
                commandments_data: null,
            }
        },
        computed: mapState({
            bible_data: state => state.inquisition.bible_data,
            data: state => state.inquisition.commandments_data,
        }),
        watch: {
            bible(val) {
                console.log(val);
                this.$store.dispatch('SELECT_BIBLE', val)
                    .then(() => {
                        this.$store.dispatch('GET_ALL_COMMANDMENTS')
                            .then(() => this.commandments_data = this.data)
                    });

            }
        },
        methods: {
            handleClose() {
                localStorage.removeItem("token");
            },
            goBack() {
               
                    this.$router.push({ name: 'auth-page' });
                
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
            this.$store.dispatch('GET_ALL_BIBLES');
            this.$store.dispatch('GET_ALL_COMMANDMENTS')
                .then(() => this.commandments_data = this.data);
        }
    }
</script>
<style >

</style>
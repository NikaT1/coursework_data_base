<template>
    <div>
        <Header />
        <div class="main-background div-block">
            <div class="div-block table-name">
                Идет процесс сбора доносов
            </div>
            <div class="div-block" id="div-inline">
                <div v-if ="is_inq" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_inq" v-on:goBack="goBack" v-on:newAcc="newAcc" v-on:finishAcc="finishAcc" />
                </div>
                <div v-if ="is_bish" class="div-inline" id="div-buttons">
                    <ButtonsBlock v-bind:buttons="buttons_for_bish" v-on:goBack="goBack" v-on:newAcc="newAcc" />
                </div>
            </div>
            <div class="div-block table-name">
                Список доносов:
            </div>
        </div>
        <div class="div-block" id="result-table">
            <AccusationResultTable v-model:data="data" />
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
    import AccusationResultTable from "@/components/pcomponents/table/AccusationResultTable";
    import Footer from "@/components/pcomponents/blocks/Footer";
    import { mapState } from 'vuex';

    export default {
        components: {
            Footer,
            Header,
            ButtonsBlock,
            AccusationResultTable,
        },
        name: 'Proccessing_accusation',
        data() {
            return {
                buttons_for_inq: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'новый донос', command: 'newAcc' },
                    { msg: 'закончить сбор доносов', command: 'finishAcc' },
                ],
                buttons_for_bish: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'новый донос', command: 'newAcc' },
                ],
                is_inq: (localStorage.getItem("role") == '0'),
                is_bish: (localStorage.getItem("role") == '1'),
            }
        },
        computed: mapState({
            data: state => state.inquisition.acc_table_data
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
                ////FIXME
            }, 
            finishAcc() {
                this.$router.push({ name: 'proccessing-cases' });
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
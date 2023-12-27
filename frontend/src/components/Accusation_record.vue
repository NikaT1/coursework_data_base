<template>
    <div id="div-main">
        <Header />
        <div class="main-background">
            <div class="table-name">
                Создание нового доноса
            </div>
            <div id="div-inline">
                <ArgsBlockRecord v-model:p_accused="p_accused" v-model:p_informer="p_informer" v-model:p_cur_violation_place="p_cur_violation_place" v-model:p_cur_date_time="p_cur_date_time" v-model:p_cur_description="p_cur_description" />
                <div>
                    <ButtonsBlock v-bind:buttons="buttons_for_new_rec" v-on:goBackToMain="goBackToMain" v-on:createNewAcc="createNewAcc" />
                </div>
            </div>
        </div>
    </div>
    <Footer />
</template>

<script>
    import Header from "@/components/pcomponents/blocks/Header";
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
    import ArgsBlockRecord from "@/components/pcomponents/blocks/ArgsBlockRecord";
    import Footer from "@/components/pcomponents/blocks/Footer";

    export default {
        components: {
            Footer,
            Header,
            ButtonsBlock,
            ArgsBlockRecord,
        },
        name: 'Accusation_record',
        data() {
            return {
                buttons_for_new_rec: [
                    { msg: 'назад', command: 'goBack' },
                    { msg: 'создать', command: 'createNewAcc' },
                ],
                p_accused: null,
                p_informer: null,
                p_cur_violation_place: "",
                p_cur_date_time: "",
                p_cur_description: "",
            }
        },
        methods: {
            handleClose() {
                localStorage.removeItem("token");
            },
            goBack() {
                    this.$router.push({ name: 'auth-page' });
               
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
                            this.p_accused = null;
                            this.p_informer = null;
                            this.p_cur_violation_place = "";
                            this.p_cur_date_time = null;
                            this.p_cur_description = "";
                            this.showInfo("Новый донос добавлен"); 
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
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: err.message,
                    type: 'error'
                });
            },
            showInfo(msg) {
                this.$notify({
                    group: "info",
                    title: 'Успешно!',
                    text: msg,
                    type: 'info'
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
</style>
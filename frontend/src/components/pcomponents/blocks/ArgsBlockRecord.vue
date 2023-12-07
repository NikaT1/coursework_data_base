<template>
    <div>
        <div class="background">
            <div class="card flex justify-content-center">
                <div>Выберите доносчика:</div>
                <Dropdown v-model="informer" :options="people_data" filter optionLabel="name" class="w-full md:w-14rem" />
                <div>Выберите обвиненного:</div>
                <Dropdown v-model="accused" :options="people_data" filter optionLabel="name" class="w-full md:w-14rem" />
            </div>
        </div>
        <div class="background">
            
            <div class="card flex justify-content-center">
                <div>Выберите дату преступления:</div>
                <Calendar v-model="cur_date_time" dateFormat="dd.mm.yy" />
                <div>Опишите место преступления:</div>
                <InputText type="text" v-model="cur_violation_place" />
            </div>
        </div>
        <div class="background">
            <div class="card flex justify-content-center">
                <div>Опишите ситуацию:</div>
                <InputText type="text" v-model="cur_description" />
            </div>
        </div>

    </div>
</template>


<script>
    import { mapState } from 'vuex';
    import Dropdown from 'primevue/dropdown';
    import Calendar from 'primevue/calendar';
    import InputText from 'primevue/inputtext';
    export default {
        name: "ArgsBlockRecord",
        components: {
            Dropdown,
            Calendar,
            InputText,
        },
        props: ['p_accused', 'p_informer', 'p_cur_violation_place', 'p_cur_date_time', 'p_cur_description'],
        emits: ['update:p_accused', 'update:p_informer', 'update:p_cur_violation_place', 'update:p_cur_date_time', 'update:p_cur_description'],
        data() {
            return {
                accused: null,
                informer: null,
                cur_violation_place: "",
                cur_date_time: "",
                cur_description: "",
            }
        },
        watch: {
            accused(val) {
                const accused = val;
                const result = this.people_data.filter((loc) => {
                    if (loc.name == accused) {
                        return loc;
                    }
                });
                this.$emit('update:p_accused', result);
            },
            informer(val) {
                const informer = val;
                const result = this.people_data.filter((bib) => {
                    if (bib.name == informer) {
                        return bib;
                    }
                });
                this.$emit('update:p_informer', result);
            },
            cur_violation_place(val) {
                this.$emit('update:p_cur_violation_place', val);
            },
            cur_date_time(val) {
                this.$emit('update:p_cur_date_time', val);
            },
            cur_description(val) {
                this.$emit('update:p_cur_description', val);
            },
        },
        created() {
            this.$store.dispatch('GET_ALL_PEOPLE');
        },
        computed: mapState({
            people_data: state => state.inquisition.people_data,
        }),

    }
</script>

<style scoped>

    .background {
        background: rgba(255, 255, 255, 0.7);
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        border-radius: 5px;
    }
</style>
<template>
    <div>
        <div class="background">
            <div class="card flex justify-content-center">
                <div>Выберите библию:</div>
                <Dropdown v-model="bible" :options="bible_data" filter optionLabel="name" class="w-full md:w-14rem" />
                <div>Выберите местность:</div>
                <Dropdown v-model="locality" :options="locality_data" filter optionLabel="name" class="w-full md:w-14rem" />
            </div>
        </div>

    </div>
</template>


<script>
    import { mapState } from 'vuex';
    import Dropdown from 'primevue/dropdown';
    
    export default {
        name: "ArgsBlockInq",
        components: {
            Dropdown,
        },
        props: ['p_locality', 'p_bible'],
        emits: ['update:p_locality', 'update:p_bible'],
        data() {
            return {
                locality: null,
                bible: null,
                filtered_locality: null,
            }
        },
        watch: {
            locality(val) {
                this.$emit('update:p_locality', val);
            },
            bible(val) {
                this.$emit('update:p_bible', val);
            },
        },
        created() {
            this.$store.dispatch('GET_ALL_BIBLES');
            this.$store.dispatch('GET_ALL_LOCALITIES');
        },
        computed: mapState({
            bible_data: state => state.inquisition.bible_data,
            locality_data: state => state.inquisition.locality_data,
        }),

    }
</script>

<style scoped>
    * {
        padding: 0% 0% 1% 1%;
    }
    .background {
        background: rgba(255, 255, 255, 0.7);
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        border-radius: 5px;
    }
</style>
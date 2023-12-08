<template>
    <div>
        <div class="background">
            <div class="card flex justify-content-center">
                <div>Выберите своды:</div>
 
                <MultiSelect v-model="commandments" :options="data" filter optionLabel="description"
                             :maxSelectedLabels="10" class="w-full md:w-20rem" />
            </div>
        </div>

    </div>
</template>


<script>
    import { mapState } from 'vuex';
    import MultiSelect from 'primevue/multiselect';
    export default {
        name: "ArgsBlockRecord",
        components: {
            MultiSelect,
        },
        props: ['p_commandments'],
        emits: ['update:p_commandments'],
        data() {
            return {
                commandments: null,
            }
        },
        watch: {
            commandments(val) {
                this.$emit('update:p_commandments', val);
            },
        },
        created() {
            this.$store.dispatch('GET_ALL_COMMANDMENTS');
        },
        computed: mapState({
            data: state => state.inquisition.commandments_data,
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
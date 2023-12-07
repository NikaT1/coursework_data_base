<template>
    <div>
        <div class="background">
            <p>Выберите библию:</p>
            <RadioBoxChain v-model:bible_data="bible_data" v-model:param_bible="bible" radio_name="bibleRadioBox" />
        </div>
        <div class="background">
            <p>Выберите местность:</p>
            <div class="card flex justify-content-center">
                <Dropdown v-model="locality" :options="locality_data" filter optionLabel="name" class="w-full md:w-14rem" />
            </div>
        </div>

    </div>
</template>


<script>
    import RadioBoxChain from "@/components/pcomponents/interactiveElements/RadioBoxChain";
    import { mapState } from 'vuex';
    import Dropdown from 'primevue/dropdown';
    export default {
        name: "ArgsBlockInq",
        components: {
            RadioBoxChain,
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
                alert(val);
                const locality = val;
                const result = this.locality_data.filter((loc) => {
                    if (loc.name == locality) {
                        return loc;
                    }
                });
                this.$emit('update:p_locality', result);
            },
            bible(val) {
                alert(val);
                const bible = val;
                const result = this.bible_data.filter((bib) => {
                    if (bib.name == bible) {
                        return bib;
                    }
                });
                this.$emit('update:p_bible', result);
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

    .background {
        background: rgba(255, 255, 255, 0.7);
        -webkit-background-size: cover;
        -moz-background-size: cover;
        -o-background-size: cover;
        border-radius: 5px;
    }
</style>
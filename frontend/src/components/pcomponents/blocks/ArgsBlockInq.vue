<template>
    <div>
        <div class="background">
            <p>Выберите библию:</p>
            <RadioBoxChain v-model:bible_data="bible_data" v-model:p_bible="bible" radio_name="bibleRadioBox" />
        </div>
        <div class="background">
            <p>Выберите местность:</p>
            <select v-model="locality">
                <option v-for="locality in locality_data" v-bind:key="locality">{{locality.name}}</option>
            </select>
        </div>
    </div>
</template>

<script>
    import RadioBoxChain from "@/components/pcomponents/interactiveElements/RadioBoxChain";
    import { mapState } from 'vuex';
    export default {
        name: "ArgsBlockInq",
        components: {
            RadioBoxChain,
        },
        props: ['p_locality', 'p_bible'],
        emits: ['update:p_locality', 'update:p_bible'],
        data() {
            return {
                locality: "",
                bible: "",
            }
        },
        watch: {
            locality(val) {
                this.$emit('update:p_locality', val);
            },
            bible(val) {
                this.$emit('update:p_bible', val);
            },
            p_locality(val) {
                this.locality = val;
            },
            p_bible(val) {
                this.bible = val;
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
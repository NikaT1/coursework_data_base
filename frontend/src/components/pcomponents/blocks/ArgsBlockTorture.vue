<template>
    <div>
        <div class="background">
            <div class="background">
                <div class="card flex justify-content-center">
                    <div>Выберите результат:</div>
                    <Dropdown v-model="result" :options="result_data" filter optionLabel="name" class="w-full md:w-14rem" />
                </div>
                <div class="card flex justify-content-center">
                    <div>Опишите, как прошла пытка:</div>
                    <InputText type="text" v-model="discription" />
                </div>
            </div>
        </div>

    </div>
</template>


<script>

    import Dropdown from 'primevue/dropdown';
    export default {
        name: "ArgsBlockTorture",
        components: {
            Dropdown,
        },
        props: ['p_result', 'p_description'],
        emits: ['update:p_result', 'update:p_description'],
        data() {
            return {
                description: "",
                result_data: [{ id: 0, name: "Не признал вину" },
                    { id: 1, name: "Признал вину" }],
                result: null,
            }
        },
        watch: {
            description(val) {
                this.$emit('update:p_description', val);
            },
            result(val) {
                this.$emit('update:p_result', val);
            },
        },
     
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
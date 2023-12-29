<template>
    <div class="info-div background">
        <p><slot></slot></p>
        <ButtonsBlock v-bind:buttons="buttons" v-on:click="click" />
    </div>
</template>

<script>
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";

    export default {
        name: "TextBlock",
        components: {
            ButtonsBlock
        },
        data() {
            return {
                buttons: [
                    { msg: this.button_msg, command: "click" },
                ],

            }
        },
        props: ['button_msg'],
    }

</script>

<style scoped>
</style>
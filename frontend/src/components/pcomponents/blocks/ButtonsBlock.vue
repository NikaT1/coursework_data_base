<template>
  <div class="buttons">
    <div class="buttons-inline" v-for="button in buttons" :key="button">
      <Button v-bind:msg="button.msg" @click="$emit(button.command)"/>
    </div>
  </div>
</template>

<script>
import Button from "@/components/pcomponents/interactiveElements/Button";

export default {
  name: "ButtonsBlock",
  components: {
    Button,
  },
  props: ['buttons']
}
</script>

<style scoped>
    .buttons {
        justify-content: center;
    }
    .buttons-inline {
        display: inline-block;
        margin: 1% 1% 0% 1%;
    }
</style>
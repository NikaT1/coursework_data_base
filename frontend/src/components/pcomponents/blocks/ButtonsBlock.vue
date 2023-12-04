<template>
  <div>
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
.buttons-inline {
  display: inline-block;
  margin: 0 2% 0 0;
}
</style>
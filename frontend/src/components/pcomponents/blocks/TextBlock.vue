<template>
  <div class="info-div background">
    <p><slot></slot></p>
    <Button v-bind:msg="button_msg" @click="$emit('click')"/>
  </div>
</template>

<script>
import Button from "@/components/pcomponents/interactiveElements/Button";

export default {
  name: "TextBlock",
  components: {
    Button
  },
  props: ['button_msg'],
}

</script>

<style scoped>

</style>
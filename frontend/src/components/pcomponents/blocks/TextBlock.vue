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

.background, .background div {
  margin: 0 auto;
  padding: 10px 10px 10px 10px;
  width: 60%;
}

.info-div * {
  margin: 10px 10px 10px 10px;
}

@media (max-width: 1228px) {
  * {
    font-size: 15px;
  }
}

@media (max-width: 892px) {
  * {
    font-size: 12px;
  }
}

</style>
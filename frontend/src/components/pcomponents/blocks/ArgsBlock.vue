<template>
  <div>
    <div class="background">
      <p>X:</p>
      <RadioBoxChain v-model:radio_data="radio_data" v-model:param_x="x" radio_name="xCheckbox"/>
    </div>
    <div>
      <p>Y:</p>
      <Input class="input-with-check" name="y" placeholder="Введите число: (-3; 3)" v-model:param="y"/>
    </div>
    <div class="background">
      <p>R:</p>
      <RadioBoxChain v-model:radio_data="radio_data" v-model:param_x="r" radio_name="rCheckbox"/>
    </div>
  </div>
</template>

<script>
import RadioBoxChain from "@/components/pcomponents/interactiveElements/RadioBoxChain";
import Input from "@/components/pcomponents/interactiveElements/Input";

export default {
  name: "ArgsBlock",
  components: {
    Input,
    RadioBoxChain,
  },
  props: ['param_x', 'param_r', 'param_y'],
  emits: ['update:param_x', 'update:param_r', 'update:param_y'],
  data() {
    return {
      radio_data: [-5, -4, -3, -2, -1, 0, 1, 2, 3],
      x: -5,
      r: 1,
      y: "",
    }
  },
  watch: {
    r(val) {
      this.$emit('update:param_r', val);
    },
    x(val) {
      this.$emit('update:param_x', val);
    },
    y(val) {
      this.$emit('update:param_y', val);
    },
    param_x(val) {
      this.x = val;
    },
    param_r(val) {
      this.r = val;
    },
    param_y(val) {
      this.y = val;
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
<template>
  <div v-for="x in radio_data" :key="x" class="labels">
    <label>
      <input v-if="x===param_x" :name="radio_name" type="radio" :value="x" checked
             @input="$emit('update:param_x', $event.target.value)">
      <input v-else :name="radio_name" type="radio" :value="x"
             @input="$emit('update:param_x', $event.target.value)">
      <p>{{ x }}</p>
    </label>
  </div>
</template>

<script>
export default {
  name: "RadioBoxChain",
  props: ['radio_data', 'param_x', 'radio_name'],
  emits: ['update:param_x'],
}
</script>

<style scoped>
.labels {
  display: inline-block;
}

.labels label {
  display: block;
  vertical-align: middle;
  margin: 10% 10% 10%;
  text-align: center;
}

@media (max-width: 1228px) {
  * {
    font-size: 14px;
  }
}

@media (max-width: 892px) {
  * {
    font-size: 13px;
  }
}
</style>
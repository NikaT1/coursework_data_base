<template>
  <div v-for="bible in bible_data" :key="bible" class="labels">
    <label>
      <input :name="radio_name" type="radio" :value="bible" checked
             @input="$emit('update:param_bible', $event.target.value)">
      <p>{{ bible.name }}</p>
    </label>
  </div>
</template>

<script>
export default {
  name: "RadioBoxChain",
  props: ['bible_data', 'param_bible', 'radio_name'],
  emits: ['update:param_bible'],
}
</script>

<style scoped>
.labels {
  display: inline-block;
}

.labels label {
  display: block;
  vertical-align: middle;
  margin: 20% 20% 20%;
  text-align: center;
}

</style>
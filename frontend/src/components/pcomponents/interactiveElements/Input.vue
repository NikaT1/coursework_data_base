<template>
  <input :type="type" :name="name" maxlength="17" autocomplete="off"
         :placeholder="placeholder" :value="param"
         @input="$emit('update:param', $event.target.value)">
</template>

<script>
export default {
  name: "Input",
  props: ['type', 'name', 'placeholder', 'param'],
  emits: ['update:param'],
}
</script>

<style scoped>
input {
  display: block;
  width: 100%;
  height: calc(2.25em + 2px);
  padding: 0.375em 0.75em 0.375em 0.75em;
  font-family: inherit;
  font-size: 1em;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  box-sizing: border-box;
  background-clip: padding-box;
  border: 1px solid #bdbdbd;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

input::placeholder {
  color: #212529;
  opacity: 0.4;
}

.error-input {
  border-color: red;
  background-color: rgba(234, 111, 145, 0.97);
}

@media (max-width: 1228px) {
  input {
    height: calc(2em + 2px);
    padding: 0.3em 0.5em 0.3em 0.5em;
    font-size: 0.8em;
    line-height: 1;
  }
}

@media (max-width: 892px) {
  input {
    height: calc(2em + 1px);
    padding: 0.2em 0.3em 0.2em 0.3em;
    font-size: 0.5em;
    line-height: 0.5;
  }
}
</style>
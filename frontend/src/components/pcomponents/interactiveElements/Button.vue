<template>
  <button class="button">
    {{msg}}
  </button>
</template>

<script>
export default {
  name: "Button",
  props: ['msg']
}
</script>

<style scoped>
.button {
  font-weight: 700;
  text-decoration: none;
  padding: .8em 5em calc(.8em + 3px);
  border-radius: 1px;
  border-width: thin;
  border-color: rgba(2, 2, 2, 0.4);
  background: rgba(181, 183, 181, 0.76);
  transition: 0.2s;
}

.button:hover {
  background: rgba(229, 229, 229, 0.73);
}

.button:active {
  outline: none;
  background: rgba(196, 192, 192, 0.73);
}
@media (max-width: 1228px) {
  button {
    font-size: 10px;
  }
}

@media (max-width: 892px) {
  button {
    font-size: 8px;
  }
}
</style>

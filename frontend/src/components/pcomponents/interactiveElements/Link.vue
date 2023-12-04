<template>
  <a :href=href>{{ name }}</a>
</template>

<script>
export default {
  name: "Link",
  props: ['href', 'name'],
}
</script>

<style scoped>
a {
  text-decoration: none
}

a:link {
  color: #ababab;
}

a:visited {
  color: #ababab;
}

a:hover {
  color: #fdfdfd;
}

a:active {
  color: #7c7c7c;
}
</style>
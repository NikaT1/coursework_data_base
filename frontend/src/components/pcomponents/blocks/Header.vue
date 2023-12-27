<template>
  <header>
    <div id="title"><h1>Испанская инквизиция</h1></div>
    <nav>
        <div class="name-div">
            Овчаренко Александр, Тройникова Вероника
        </div>
        <div class="variant-div">
            Группа Р33302
        </div>
    </nav>
  </header>
</template>

<script>

export default {
  name: "Header",
}
</script>

<style scoped>
header {
  font-size: 12px;
  display: table;
  padding: 0.5em 1% 0.5% 1%;
  background: #55555d;
  color: #cac8c8;
  width: 100%;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  alignment: left;
}

header nav {
  display: table-cell;
  vertical-align: 10px;
  text-align: right;
  color: #ababab;
}

header nav a {
  margin: 0 0 5% 5%;
  font-size: larger;
}

.name-div, .variant-div {
  font-size: medium;
  color: #ababab;
}

#title {
  background: #413f47;
  margin: 0 0 1% 0;
  width: fit-content;
  padding: 1em 1em 1em 1em;
  border-radius: 2px;
}

</style>

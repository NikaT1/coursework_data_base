<template>
  <footer>
    <div><p>Студентческий проект по предмету <br/> "Информационные системы и базы данных"</p></div>
    <nav>
      <Link href="https://itmo.ru/" name="Университет ИТМО"/>
    </nav>
  </footer>
</template>

<script>
import Link from "@/components/pcomponents/interactiveElements/Link";
export default {
  name: "Footer",
  components: {Link}
}
</script>

<style scoped>
footer {
  font-size: medium;
  display: table;
  padding: 2em 5% 2% 5%;
  background: #55555d;
  color: #cac8c8;
  width: 100%;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  alignment: left;
}

div p {
  color: #cac8c8;
  font-size: larger;
}

footer nav {
  display: table-cell;
  vertical-align: middle;
  text-align: right;
  color: #ababab;
}

footer nav a {
  margin: 0 0 5% 5%;
  font-size: larger;
}

@media (max-width: 1228px) {
  div {
    font-size: 20px;
    padding: 6px;
    border-radius: 6px;
    border-spacing: 6px;
  }

}

@media (max-width: 892px) {
  div {
    font-size: 16px;
    padding: 4px;
    border-radius: 4px;
    border-spacing: 4px;
  }

}
</style>

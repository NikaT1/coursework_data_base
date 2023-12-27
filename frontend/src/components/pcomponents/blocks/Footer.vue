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
        height: 50px;
        font-size: 12px;
        display: table;
        padding: 1em 3% 1% 3%;
        background: #55555d;
        color: #cac8c8;
        width: 100%;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
        alignment: left;
    }

div p {
  color: #cac8c8;
  font-size: 14px;
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

</style>

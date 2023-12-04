<template>
  <div id="app">
    <notifications class="notify" group="error" position="top right" max="6" close-on-click width="30%"/>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>
<style>

* { padding: 0; margin: 0; }

html, body {
  background-color: #ffffff;
  width: 100%;
  height: 100%;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell,
  "Fira Sans", "Droid Sans", Helvetica, Arial, sans-serif;
}

.main-background {
  background: linear-gradient(rgba(234, 230, 230, 0.15), rgba(252, 251, 251, 0.15)),
  url("assets/background.jpg") center/cover;
}

.background {
  background: rgba(255, 255, 255, 0.7);
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  border-radius: 5px;
}

#app {
  width: 100%;
  height: 100%;
}

input[type="text"] {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  margin: 0;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
textarea:-webkit-autofill,
textarea:-webkit-autofill:hover,
textarea:-webkit-autofill:focus,
select:-webkit-autofill,
select:-webkit-autofill:hover,
select:-webkit-autofill:focus {
  border: 1px solid #bdbdbd;
  -webkit-text-fill-color: #212529;
  -webkit-box-shadow: 0 0 0px 1000px #fff inset;
  transition: background-color 5000s ease-in-out 0s;
}

.notify {
  font-family: New Century Schoolbook, TeX Gyre Schola, serif;
  font-size: 30px;
}

p {
  color: #2b2b2b;
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  box-shadow: inset 0 0 6px rgba(86, 85, 86, 0.49);
}

::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 6px rgba(101, 98, 102, 0.49);
}

@media (max-width: 1228px) {
  * {
    font-size: 20px;
    padding: 6px;
  }
}

@media (max-width: 892px) {
  * {
    font-size: 16px;
    padding: 4px;
  }
}

</style>
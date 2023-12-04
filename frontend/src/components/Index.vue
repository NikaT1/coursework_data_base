<template>

  <div class="main-background" id="main-div">
    <Header/>
    <div class="div-block">
      <TextBlock v-if="info" v-on:click="start($event)" button_msg="Начать">
        Скрипт определяет попадание точки на координатной плоскости в заданную область. <br><br>
        Параметр R и координаты точки задаются с помощью полей ввода или графика. Итоговая таблица содержит полученные
        параметры и результат вычислений - факт попадания или непопадания точки в область.
      </TextBlock>
      <AccountBlock v-if="account" v-model:login="login" v-model:password="password"
                    v-on:createUser="createUser($event)"
                    v-on:logIn="logIn($event)"/>
    </div>
  </div>
  <Footer/>
</template>

<script>
import Header from "@/components/pcomponents/blocks/Header";
import TextBlock from "@/components/pcomponents/blocks/TextBlock";
import AccountBlock from "@/components/pcomponents/blocks/AccountBlock";
import Footer from "@/components/pcomponents/blocks/Footer";

export default {
  components: {
    Footer,
    Header,
    TextBlock,
    AccountBlock,
  },
  name: "Index",
  data() {
    return {
      login: "",
      password: "",
      account: false,
      info: true,
    }
  },
  beforeMount() {
    localStorage.removeItem('par');
  },
  methods: {
    createUser() {
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: this.login, password: this.password})
      };
      this.sendRequest(requestOptions, "/api/user/new-user");

    },
    logIn() {
      const requestOptions = {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: this.login, password: this.password})
      };
      this.sendRequest(requestOptions, "/api/user/check-user");
    },
    start() {
      this.account = true
      this.info = false
    },
    sendRequest(requestOptions, addr) {
      fetch(addr, requestOptions)
          .then(response => {
            if (response.ok) return response.text();
            else {
              return response.text().then(text => {
                throw new Error(text)
              });
            }
          }).then(data => {
        localStorage.setItem("par", data);
        this.$router.push({name: 'main-page'});
      }).catch((e) => {
        localStorage.removeItem("par");
        this.$notify({
          group: 'error',
          title: 'Ошибка',
          text: e.message,
          type: 'error'
        });
      });
    }
  }
}
</script>

<style scoped>

#main-div {
  min-width: 100%;
  min-height: 100%;
  position: relative;
}

.div-block {
  display: block;
  margin: 6% 0 0 0;
}
</style>
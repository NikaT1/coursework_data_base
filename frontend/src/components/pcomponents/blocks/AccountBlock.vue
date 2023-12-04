<template>
  <div class="background" id="account">
    <div class="title">
      <h2>Вход в аккаунт</h2>
    </div>
    <div>
      <h3>Логин</h3>
      <Input type="text" id="loginInput" placeholder="Username" :value="login"
             @input="$emit('update:login', $event.target.value)"/>
      <h3>Пароль</h3>
      <Input type="password" id="password" placeholder="Password" :value="password"
             @input="$emit('update:password', $event.target.value)"/>
    </div>
    <ButtonsBlock v-bind:buttons="buttons" v-on:logIn="$emit('logIn')" v-on:createUser="$emit('createUser')"/>
  </div>
</template>

<script>
import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
import Input from "@/components/pcomponents/interactiveElements/Input";

export default {
  name: "AccountBlock",
  props: ['login', 'password'],
  emits: ['update:login', 'update:password'],
  components: {
    Input,
    ButtonsBlock
  },
  data() {
    return {
      buttons: [
        {msg: "Войти", command: "logIn"},
        {msg: "Создать", command: "createUser"}
      ]
    }
  }
}
</script>

<style scoped>

.background, .background div {
  margin: 0 auto;
  padding: 10px 10px 10px 10px;
  width: 60%;
}

.background div input {
  margin: 10px 0;
}

.background div Button {
  margin: 0;
}

.title {
  text-align: center;
}

@media (max-width: 1228px) {
  #password, #loginInput {
    font-size: 10px;
  }
}

@media (max-width: 892px) {
  #password, #loginInput {
    font-size: 8px;
  }
}
</style>
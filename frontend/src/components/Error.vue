<template>
  <div id="main-div" class="main-background">
    <div class="div-block">
      <img id="error-img" src="../assets/error-img.png" alt="Error image"/>
    </div>
    <div class="div-block">
      <TextBlock button_msg="На главную" v-on:click="goToStart">
        Что-то пошло не так... Вернитесь, пожалуйста, на стартовую страницу
      </TextBlock>
    </div>
  </div>
</template>

<script>
import TextBlock from "@/components/pcomponents/blocks/TextBlock";

export default {
  name: "NotFoundError",
  components: {TextBlock},
  props: {
    errorCode: String,
    errorMessage: String,
  },
  methods: {
    goToStart() {
      localStorage.removeItem("par");
      this.$router.push({name: 'auth-page'});
    },
  }
}

</script>

<style scoped>

#error-img {
  object-fit: contain;
  object-position: center;
  width: 35%;
  height: 35%;
  display: block;
  margin: 0 auto;
}

#main-div {
  font-size: large;
  min-width: 100%;
  min-height: 100%;
  position: relative;
}

.div-block {
  display: block;
  margin: 1% 0 0 0;
}

.background, .background div {
  margin: 0 auto;
  padding: 10px 10px 10px 10px;
  width: 40%;
}

</style>
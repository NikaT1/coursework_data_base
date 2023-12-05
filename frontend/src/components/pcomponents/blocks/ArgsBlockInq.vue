<template>
  <div>
    <div class="background">
      <p>Выберите библию:</p>
      <RadioBoxChain v-model:bible_data="bible_data" v-model:param_bible="bible" radio_name="bibleRadioBox"/>
    </div>
    <div class="background">
      <p>Выберите местность:</p>
      <select v-model="locality">
          <option v-for="locality in locality_data" v-bind:key="locality">{{locality.name}}</option>
      </select>
    </div>
  </div>
</template>

<script>
import RadioBoxChain from "@/components/pcomponents/interactiveElements/RadioBoxChain";

export default {
  name: "ArgsBlockInq",
  components: {
    RadioBoxChain,
  },
  props: ['param_locality', 'param_bible'],
  emits: ['update:param_locality', 'update:param_bible'],
  data() {
    return {
        bible_data: [
            { name: 'Библия 1', id: 1 },
            { name: 'Библия 2', id: 2 },
            { name: 'Библия 3', id: 3 }
        ],
        locality_data: [
            { name: 'Санкт-Петербург', id: 1 },
            { name: 'Нижжжжжний', id: 2 }
        ],
      locality: "",
      bible: "",
    }
  },
  watch: {
    locality(val) {
      this.$emit('update:param_locality', val);
    },
    bible(val) {
      this.$emit('update:param_bible', val);
    },
    param_locality(val) {
      this.locality = val;
    },
    param_bible(val) {
      this.bible = val;
    },
  },
  method: {
      loadData() {
          this.bible_data = [
              { name: 'Библия 1', id: 1 },
              { name: 'Библия 2', id: 2 },
              { name: 'Библия 3', id: 3 }
          ];
          this.locality_data = [
              { name: 'Санкт-Петербург', id: 1 },
              { name: 'Нижжжжжний', id: 2 }
          ];
          //const requestOptions = {
          //    method: "GET",
          //    headers: { "Authorization": "Bearer " + localStorage.getItem("par") },
          //};
          //const address = "*******************";
          //this.sendRequestWithLocalityData(address, requestOptions);
          //address = "*******************";
          //this.sendRequestWithBibleData(address, requestOptions);
      },
      sendRequestWithLocalityData(address, requestOptions) {
          fetch(address, requestOptions)
              .then(response => {
                  if (response.ok) return response.json();
                  else {
                      return response.text().then(text => {
                          throw new Error(text)
                      });
                  }
              }).then(data => {
                  this.locality_data = data;
              }).catch((e) => {
                  this.showError(e.message);
              });
      },
      sendRequestWithBibleData(address, requestOptions) {
          fetch(address, requestOptions)
              .then(response => {
                  if (response.ok) return response.json();
                  else {
                      return response.text().then(text => {
                          throw new Error(text)
                      });
                  }
              }).then(data => {
                  this.bible_data = data;
              }).catch((e) => {
                  this.showError(e.message);
              });
      },
  },
  mounted() {
    this.loadData();
  }
}
</script>

<style scoped>

.background {
  background: rgba(255, 255, 255, 0.7);
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  border-radius: 5px;
}

</style>
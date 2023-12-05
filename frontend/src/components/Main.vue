<template>
  <div>
    <Header/>
    <div class="main-background div-block">
        <div class="div-block" id="div-inline">
            <ArgsBlockInq v-if="new_inq" class="div-block" v-model:param_x="param_x" v-model:param_r="param_r" v-model:param_y="param_y" />

            <div v-if="main_info" class="div-inline" id="div-buttons">
                <ButtonsBlock v-bind:buttons="start_buttons" v-on:goBack="goBack" v-on:startNew="startNew" v-on:openCurrent="openCurrent" />
            </div>
            <div v-if="new_inq" class="div-inline" id="div-buttons">
                <ButtonsBlock v-bind:buttons="new_inq_buttons" v-on:goBack="goBack" v-on:startNew="startNew" />
            </div>
        </div>
      <div v-if="main_info" class="div-block table-name">
          Список прошлых инквизиционных процессов:
      </div>
    </div>
    <div v-if="main_info" class="div-block" id="result-table">
      <ResultTable v-model:data="data"/>
    </div>
  </div>
  <Footer/>
</template>

<script>
import Header from "@/components/pcomponents/blocks/Header";
import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
import ResultTable from "@/components/pcomponents/table/InquisitionResultTable";
import Footer from "@/components/pcomponents/blocks/Footer";
import ArgsBlockInq from "@/components/pcomponents/blocks/ArgsBlockInq";

export default {
  components: {
    Footer,
    Header,
    ButtonsBlock,
    ResultTable,
    ArgsBlockInq,
  },
  name: 'Main',
  data() {
    return {
      data: new Array(0),
      start_buttons: [
        {msg: 'выйти', command: 'goBack'},
        {msg: 'новый инквизиционный процесс', command: 'startNew'},
        {msg: 'текущий инквизиционный процесс', command: 'openCurrent'}
      ],
      new_inq_buttons: [
        { msg: 'создать', command: 'startNew' },
        {msg: 'выйти', command: 'goBack'}
      ],
      new_inq: false,
      main_info: true,
    }
  },
  created: function () {
    document.addEventListener('beforeunload', this.handlerClose);
  },
  methods: {
    handleClose() {
      localStorage.removeItem("par");
    },
    goBack() {
      localStorage.removeItem("par");
      this.$router.push({name: 'auth-page'});
    },
    startNew() {
        this.new_inq = true;
        this.main_info = false;
    },
    openCurrent() {
      this.$router.push({name: 'auth-page'});
    },
    loadData() {
      const requestOptions = {
        method: "GET",
        headers: {"Authorization": "Bearer " + localStorage.getItem("par")},
      };
      const address = "*******************";
      this.sendRequestWithData(address, requestOptions);
    },
    sendRequestWithData(address, requestOptions) {
      fetch(address, requestOptions)
          .then(response => {
            if (response.ok) return response.json();
            else {
              return response.text().then(text => {
                throw new Error(text)
              });
            }
          }).then(data => {
        this.data = data;
      }).catch((e) => {
        this.showError(e.message);
      });
    },
    showError(text) {
      this.$notify({
        group: "error",
        title: 'Ошибка',
        text: text,
        type: 'error'
      });
    }
  },
  mounted() {
    this.loadData();
  }
}
</script>
<style>

.table-name {
   font-size: big;
   color: #6d747f;
   font-size: 20px;
   padding: 20px;
   font-weight: bold;
}
#div-inline div {
  vertical-align: middle;
  margin: 20px 20px 20px;
  text-align: center;
}

.main-background > div:first-child {
  display: table;
  margin: 0 auto;
}

#result-table {
  overflow-x: auto;
  height: 300px;
  margin: 10px 20px;
}

.div-block {
  display: block;
}

.div-inline {
  display: inline-block;
}

#div-buttons {
  padding: 1.5% 1.5% 1.5% 1.5%;
}

@media (max-width: 1228px) {
  #div-inline div {
    margin: 10px 10px 10px;
  }
}

@media (max-width: 892px) {
  #div-inline div {
    margin: 5px 5px 5px;
  }
}
</style>
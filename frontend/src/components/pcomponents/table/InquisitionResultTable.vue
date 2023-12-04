<template>
  <table>
    <thead>
    <tr>
      <th id="real-time">Дата начала</th>
      <th id="X">Местность</th>
      <th id="Y">Инквизитор</th>
      <th id="R">Кол-во дел</th>
      <th id="flag">Дата окончания</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="el in data" :key="el">
      <td>{{ el.start_time }}</td>
      <td>{{ el.locality }}</td>
      <td>{{ el.inquisitor }}</td>
      <td>{{ el.cases_count }}</td>
      <td>{{ el.end_time }}</td>
    </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "ResultTable",
  props: ['data'],
}
</script>

<style scoped>

table {
  color: #6d747f;
  font-size: 26px;
  font-family: New Century Schoolbook, TeX Gyre Schola, serif;
  margin: auto;
  padding: 10px;
  border-radius: 10px;
  border-spacing: 10px;
  table-layout: auto;
}

table {
  border-collapse: collapse;
  text-align: center;
  border: 4px solid rgba(79, 72, 91, 0.6);
  font-size: 20px;
  width: 100%;
  table-layout: fixed;
}

td {
  border-collapse: collapse;
  border: 4px solid rgba(79, 72, 91, 0.6);
  font-size: 20px;
}

th {
  border-collapse: collapse;
  border: 4px solid rgba(79, 72, 91, 0.6);
  font-size: 20px;
}

table::first-line {
  text-transform: uppercase;
  font-weight: bold;
}

@media (max-width: 1228px) {
  table {
    font-size: 26px;
    padding: 10px;
    border-radius: 10px;
    border-spacing: 10px;
  }

  th, td {
    font-size: 20px;
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
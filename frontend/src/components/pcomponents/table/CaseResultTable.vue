<template>
    <table>
        <thead>
            <tr>
                <th>Доносчик</th>
                <th>Епископ</th>
                <th>Обвиненный</th>
                <th>Место преступления</th>
                <th>Дата</th>
                <th>Описание</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="el in data" :key="el">
                <td>{{ el.informer }}</td>
                <td>{{ el.bishop }}</td>
                <td>{{ el.accused }}</td>
                <td>{{ el.violation_place }}</td>
                <td>{{ el.date_time }}</td>
                <td>{{ el.description }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    export default {
        name: "AccusationResultTable",
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
<template>
    <div id="app">
        <notifications class="notify" group="error" position="top right" max="6" close-on-click width="30%" />
        <router-view />
    </div>
</template>

<script>
    export default {
        name: 'App',
    }
</script>
<style>

    * {
        padding: 0;
        margin: 0;
    }

    html, body {
        background-color: #ffffff;
        width: 100%;
        height: 100%;
        font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", Helvetica, Arial, sans-serif;
    }

    .main-background {
        background: linear-gradient(rgba(234, 230, 230, 0.15), rgba(252, 251, 251, 0.15)), url("assets/background.jpg") center/cover;
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
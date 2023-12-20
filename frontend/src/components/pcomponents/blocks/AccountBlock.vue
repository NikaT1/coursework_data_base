<template>
    <div class="background" id="account">
        <div class="title">
            <h2 v-if="!new_acc">Вход в аккаунт</h2>
            <h2 v-if="new_acc">Создание аккаунта</h2>
        </div>
        <div>
            <div class="card flex justify-content-center">
                <div v-if="new_acc">Введите имя:</div>
                <InputText v-if="new_acc" type="text" v-model="name" />
                <div v-if="new_acc">Введите фамилию:</div>
                <InputText v-if="new_acc" type="text" v-model="surname" />
            </div>
            <div class="card flex justify-content-center">
                <div>Логин</div>
                <InputText type="text" v-model="login" />
                <div>Пароль</div>
                <InputText type="password" v-model="password" />
            </div>
            <div class="card flex justify-content-center">
                <div v-if="new_acc">Выберите местность:</div>
                <Dropdown v-if="new_acc" v-model="locality" :options="locality_data" filter optionLabel="name" class="w-full md:w-14rem" />
                <div v-if="new_acc">Выберите пол:</div>
                <Dropdown v-if="new_acc" v-model="gender" :options="gender_data" filter optionLabel="msg" class="w-full md:w-14rem" />
            </div>
            <div class="card flex justify-content-center">
                <div v-if="new_acc">Дата рождения:</div>
                <Calendar v-if="new_acc" v-model="birthday" dateFormat="dd.mm.yy" />
            </div>
        </div>
        <ButtonsBlock v-if="!new_acc" v-bind:buttons="buttons" v-on:logIn="logIn" v-on:createUser="createUser" />
        <ButtonsBlock v-if="new_acc" v-bind:buttons="buttons_for_new_user" v-on:goBack="goBack" v-on:addUser="addUser" />
    </div>
</template>

<script>
    import ButtonsBlock from "@/components/pcomponents/blocks/ButtonsBlock";
    import Dropdown from 'primevue/dropdown';
    import Calendar from 'primevue/calendar';
    import InputText from 'primevue/inputtext';
    import { mapState } from 'vuex';

    export default {
        name: "AccountBlock",
        components: {
            Dropdown,
            ButtonsBlock,
            Calendar,
            InputText,

        },
        data() {
            return {
                buttons: [
                    { msg: "Войти", command: "logIn" },
                    { msg: "Создать", command: "createUser" }
                ],
                buttons_for_new_user: [
                    { msg: "Назад", command: "goBack" },
                    { msg: "Создать аккаунт", command: "addUser" }
                ],
                new_acc: false,
                birthday: "",
                name: "",
                surname: "",
                login: "",
                password: "",
                gender: null,
                locality: null,
                gender_data: [{ msg: "Мужской", code: "M" }, { msg: "Женский", code: "F" }],

            }
        },
        methods: {
            createUser() {
                this.new_acc = true;
            },
            goBack() {
                this.new_acc = false;
            },
            addUser() {
                const name = this.name;
                const surname = this.surname;
                const birthDate = this.birthday;
                const personGender = this.gender.code;
                const locality = this.locality.id;
                const username = this.login;
                const password = this.password;
                
                this.$store.dispatch('CREATE_NEW_ACCOUNT', { name, surname, birthDate, personGender, locality, username, password })
                    .then(resp => {
                        localStorage.setItem("token", resp.data.token);
                        localStorage.setItem("role", resp.data.role);
                        this.$store.dispatch('GET_CUR_INQ');
                        this.$router.push({ name: 'main-inquisitor-page' });
                    },
                        err => (this.showError(err)));

            },
            logIn() {
                const username = this.login;
                const password = this.password;
                this.$store.dispatch('LOG_IN_ACCOUNT', { username, password })
                    .then(resp => {
                        localStorage.setItem("token", resp.data.token);
                        localStorage.setItem("role", resp.data.role);
                        this.$store.dispatch('GET_CUR_INQ');
                        this.$router.push({ name: 'main-inquisitor-page' });
                    },
                        err => {
                            this.showError(err);
                            localStorage.setItem("token", "rjkfgvc");
                            localStorage.setItem("role", 0);
                            this.$store.dispatch('GET_CUR_INQ');
                            this.$router.push({ name: 'main-inquisitor-page' });
                        });
                
            },

            showError(err) {
                console.log(err);
                let text = "Произошла непредвиденная ошибка";
                if (err.code == 500 || err.response.status == 500) {
                    text = "Проблема с подключением к серверу";
                }
                if (err.code == 404 || err.response.status == 404) {
                    text = "Неверный запрос к серверу";
                }
                if (err.code == 401 || err.response.status == 401) {
                    text = "Данного аккаунта не существует";
                }
                this.$notify({
                    group: "error",
                    title: 'Ошибка',
                    text: text,
                    type: 'error'
                });
            }
        },
        created() {
            this.$store.dispatch('GET_ALL_LOCALITIES');
        },
        computed: mapState({
            locality_data: state => state.inquisition.locality_data,
            token: state => state.inquisition.token,
            role: state => state.inquisition.role,
            name: state => state.inquisition.person_name,
        }),
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
//import axios from 'axios';
const state = () => ({
    cur_inq: { step: localStorage.getItem('step') || 0 },
    token: localStorage.getItem('token') || '',

    person_id: 0,
    official_id: 0,
    person_name: "",

    accusation_id: 0,
    inq_table_data: [],
    acc_table_data: [],
    acc_nr_table_data: [],
    cases_data: [],
    locality_data: [],
    bible_data: [],
    people_data: [],
    commandments_data: [],
});
const getters = {
    CUR_INQ: state => {
        return state.cur_inq;
    },
    CUR_OFFICIAL: state => {
        return state.official_id;
    },
    CUR_NAME: state => {
        return state.person_name;
    },
    ACC_TABLE_DATA: state => {
        return state.acc_table_data;
    },
};

const mutations = {
    SET_INITIAL_INF: (state, payload) => {
        state.person_id = payload.person_id;
        state.official_id = payload.official_id;
        state.person_name = payload.person_name;
    },

    SET_ACCUSATION_ID: (state, payload) => {
        state.accusation_id = payload;
    },

    SET_CUR_INQ: (state, payload) => {
        state.cur_inq = payload;
    },
    SET_OFFICIAL_ID: (state, payload) => {
        state.official_id = payload;
    },
    SET_ACC_TABLE_DATA: (state, payload) => {
        state.acc_table_data = payload;
    },
    SET_ACC_NR_TABLE_DATA: (state, payload) => {
        state.acc_nr_table_data = payload;
    },
    SET_INQ_TABLE_DATA: (state, payload) => {
        state.inq_table_data = payload;
    },
    SET_LOCALITY_DATA: (state, payload) => {
        state.locality_data = payload;
    },
    SET_BIBLE_DATA: (state, payload) => {
        state.bible_data = payload;
    },
    SET_CASES_DATA: (state, payload) => {
        state.cases_data = payload;
    },
    SET_PEOPLE_DATA: (state, payload) => {
        state.people_data = payload;
    },
    ADD_TO_ACC_TABLE_DATA: (state, payload) => {
        state.acc_table_data.push(payload);
    },
    SET_COMMANDMENTS_DATA: (state, payload) => {
        state.commandments_data = payload;
    },
};

const actions = {
    INCREASE_STEP(context) {
        const inq = context.getters.CUR_INQ;
        inq.step = inq.step + 1;
        context.commit('SET_CUR_INQ', inq);
    },

    // token -> id person, official id, person_name (то есть full_name = name+surname)
    INITIAL_ACT(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'GET' })
                .then(resp => {
                    context.commit('SET_INITIAL_INF', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/  //пока заглушка
        context.commit('SET_INITIAL_INF', {
            person_id: 1,
            official_id: 1,
            person_name: "МАРИНА НИКОЛАЕВНА",
        });
        console.log(payload)
    },
    // bible_id, locality_id -> id inq
    CREATE_NEW_INQ(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'POST' })
                .then(resp => {
                    context.commit('SET_CUR_INQ', {
                        id: resp.data.id,
                        bible: payload.bible,
                        locality: payload.locality,
                        step: 0
                    });
                    localStorage.setItem("step", "0");
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/  //пока заглушка
        console.log(payload.bible, payload.locality);
        context.commit('SET_CUR_INQ', {
            id: 1,
            bible: payload.bible,
            locality: payload.locality,
            step: 0
        });
        localStorage.setItem("step", "0");

    },
    // по official_id определяет текущую иквизицию и возвращает инфу о ней (id, bible (id, name), locality (id, name), step).
    //step - это этап, на котором находится иквизиция (0 - только создана, 1 - процесс сбора доносов запущен, 2 - процесс сбора доносов окончен (этап формирования дел)
    // 3 - это этап, когда все дела сформированы (функция get_not_resolved_cases) ничего не возвращает, 4 - все дела закончены, инквизиционный процесс завершен)
    GET_CUR_INQ(context) {
        /*return new Promise((resolve, reject) => {
            const official_id = state.official_id;
            axios({ url: '*********', data: official_id, method: 'GET' })
                .then(resp => {
                    context.commit('SET_CUR_INQ', {
                        id: resp.data.id,
                        bible: resp.data.bible,
                        locality: resp.data.locality,
                        step: resp.data.step
                    });
                    localStorage.setItem("step", resp.data.step);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/  //пока заглушка
        context.commit('SET_CUR_INQ', {
            id: 1,
            bible: "Библия 1",
            locality: "Нижжжний",
            step: 2
        });
        localStorage.setItem("step", "2");
    },

    // inq_id -> вызвать start_accusation_process и вернуть id
    START_ACCUSATION_PROCESS(context) {
        /*return new Promise((resolve, reject) => {
            const inq_id = state.cur_inq.id;
            axios({ url: '*********', data: inq_id, method: 'GET' })
                .then(resp => {
                    context.commit('SET_ACCUSATION_ID', resp.data);
                    context.dispatch('INCREASE_STEP');
                    localStorage.setItem("step", context.getters.CUR_INQ.step);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        context.commit('SET_ACCUSATION_ID', 3);
        context.dispatch('INCREASE_STEP');
        localStorage.setItem("step", context.getters.CUR_INQ.step);
    },

    // accusation_id -> все рекорды, относящиеся к этому процессу сбора доносов в виде массива json (см ниже в методе пример данных)
    GET_ALL_ACCUSATION_RECORDS(context) {
        /*return new Promise((resolve, reject) => {
            const accusation_id = state.accusation_id;
            axios({ url: '*********', data: accusation_id, method: 'GET' })
                .then(resp => {
                    context.commit('SET_ACC_TABLE_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        context.commit('SET_ACC_TABLE_DATA', [{
            id: 1,
            informer: 'Виктор Викторович',
            bishop: 'Виктор Викторович',
            accused: 'Сергей Сергеевич',
            violation_place: 'дома',
            date_time: '2023-12-23',
            description: 'бла бла бля',
        }]);
        console.log(context.getters.ACC_TABLE_DATA);
    },

    // ничего не дается на вход -> все записи об инквизициях в формате см. ниже в методе
    GET_ALL_INQUISITIONS(context) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', method: 'GET' })
                .then(resp => {
                    context.commit('SET_INQ_TABLE_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        context.commit('SET_INQ_TABLE_DATA', [{
            start_time: '2023-12-23',
            locality: 'Лесогорск',
            inquisitor: 'Сергей Сергеевич',
            cases_count: 25,
            end_time: '2023-12-25',
        }]);
    },

    // accusation_id -> вызвать finish_accusation_process, ничего не возвращать 
    FINISH_ACCUSATION_PROCESS(context) {
        /*return new Promise((resolve, reject) => {
            const inq_id = state.cur_inq.id;
            axios({ url: '*********', data: inq_id, method: 'GET' })
                .then(resp => {
                    context.dispatch('INCREASE_STEP');
                    localStorage.setItem("step", context.getters.CUR_INQ.step);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        context.dispatch('INCREASE_STEP');
        localStorage.setItem("step", context.getters.CUR_INQ.step);
    },

    // ничего на вход -> массив инфы о всех библиях см ниже формат
    GET_ALL_BIBLES(context) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', method: 'GET' })
                .then(resp => {
                    context.commit('SET_BIBLE_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка

        context.commit('SET_BIBLE_DATA', [
            { name: 'Библия 1', id: 1 },
            { name: 'Библия 2', id: 2 },
            { name: 'Библия 3', id: 3 }]);
    },

    // ничего на вход -> массив инфы о всех местностях (locality) см ниже формат
    GET_ALL_LOCALITIES(context) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', method: 'GET' })
                .then(resp => {
                    context.commit('SET_LOCALITY_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        context.commit('SET_LOCALITY_DATA', [
            { name: 'Санкт-Петербург', id: 1 },
            { name: 'Нижжжжжний', id: 2 }
        ]);
    },
    // на вход accusation_id -> вызвать get_not_resolved_accusation_record и вернуть результат (в формате как для GET_ALL_ACCUSATION_RECORDS)
    GET_NR_ACCUSATION_RECORDS(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'GET' })
                .then(resp => {
                    context.commit('SET_ACC_NR_TABLE_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
        context.commit('SET_ACC_NR_TABLE_DATA', context.getters.ACC_TABLE_DATA);
    },

    // на вход inq_id ->  вызвать finish_accusation_proccess, generate_cases, возвращать ничего не нужно
    FINISH_RESOLVING_RECORDS(context) {
        /*return new Promise((resolve, reject) => {
            const inq_id = context.getters.CUR_INQ.id;
            axios({ url: '*********', data: inq_id, method: 'GET' })
                .then(resp => {
                    context.commit('SET_CASES_DATA', resp.data);
                    context.dispatch('INCREASE_STEP');
                    localStorage.setItem("step", context.getters.CUR_INQ.step);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        context.dispatch('INCREASE_STEP');
        localStorage.setItem("step", context.getters.CUR_INQ.step);
    },

    // на вход inq_id -> вернуть все дела этой инквизиции (формат см ниже, violation_description - это конкатенация всех согрешений челикса)
    GET_ALL_CASES(context) {
        /*return new Promise((resolve, reject) => {
            const inq_id = context.getters.CUR_INQ.id;
            axios({ url: '*********', data: inq_id, method: 'GET' })
                .then(resp => {
                    context.commit('SET_CASES_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка

        context.commit('SET_CASES_DATA', [{
            id: 1,
            accused: 'Сергей Сергеевич',
            creation_date: '2023-12-23',
            violation_description: 'бла бла бля',
        }]);
    },
    // на вход id locality ->  вернуть массив всех людей (формат см ниже)
    GET_ALL_PEOPLE(context, payload) {
        /*return new Promise((resolve, reject) => {
            const locality_id = state.cur_data.locality
            axios({ url: '*********', data: payload, method: 'GET' })
                .then(resp => {
                    context.commit('SET_PEOPLE_DATA', resp.data); // FIXME concat name and surname
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
        context.commit('SET_PEOPLE_DATA', [{
            id: 1,
            name: 'Сергей',
            surname: 'Сергеевич',
        }]);
    },
    /* на вход эта инфа в виде json:
    let accused = p_accused.id;
    let bishop = bishop id;
    let informer = p_informer.id;
    let violation_place = p_cur_violation_place;
    let date_time = p_cur_date_time;
    let description = p_cur_description; 
    + inq id
    -> вызвать add_accusation_record и вернуть обновленный массив рекордов для этой инквизиции??? или обновление отдельно сделаем??*/
    ADD_ACC_RECORD(context, payload) {
        /*return new Promise((resolve, reject) => {
            payload["inq_id"] = state.cur_inq.id;
            payload["bishop"] = state.official.id;
            axios({ url: '*********', data: payload, method: 'POST' })
                .then(resp => {
                    context.commit('SET_ACC_TABLE_DATA', resp.data); 
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
        payload["bishop"] = context.getters.CUR_NAME;
        payload["id"] = 3;
        context.commit('ADD_TO_ACC_TABLE_DATA', payload);
        console.log(context.getters.ACC_TABLE_DATA);
    },

    // на вход id bible ->  вернуть массив всех commandment (вызвать функцию read_bible) (формат см ниже)
    GET_ALL_COMMANDMENTS(context, payload) {
        /*return new Promise((resolve, reject) => {
            const locality_id = state.cur_inq.bible
            axios({ url: '*********', data: payload, method: 'GET' })
                .then(resp => {
                    context.commit('SET_COMMANDMENTS_DATA', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
        context.commit('SET_COMMANDMENTS_DATA', [{
            id: 1,
            description: 'не убей',
        },
        {
            id: 2,
            description: 'не укради',
        }]);
    },
    // { commandments_id: Array(), record_id: 5 } -> ничего возвращать не нужно
    CONNECT_COMMANDMENT(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'POST' })
                .then(resp => {
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
    },
};
export default {
    state,
    getters,
    mutations,
    actions,
};
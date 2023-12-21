import axios from 'axios';
const state = () => ({

    role: -1,
    token: localStorage.getItem('token') || '',
    cur_inq: { step: localStorage.getItem('step') || 0 },

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
    queue_for_discussion: [],
    queue_for_torture: [],
    queue_for_puniishment: [],
});
const getters = {
    CUR_BIBLE: state => {
        return state.cur_inq.bible;
    },
    CUR_LOCALITY: state => {
        return state.cur_inq.locality;
    },
    CUR_INQ: state => {
        return state.cur_inq;
    },
    CUR_OFFICIAL: state => {  
        return state.official_id;
    },
    CUR_ACCUSATION: state => {
        return state.accusation_id;
    },
    CUR_NAME: state => {
        return state.person_name;
    },
    ACC_TABLE_DATA: state => {
        return state.acc_table_data;
    },
    CUR_ROLE: state => {
        return state.role;
    },
    CUR_TOKEN: state => {
        return state.token;
    },
};

const mutations = {
    SET_INITIAL_INF: (state, payload) => {
        console.log(payload)
        state.person_id = payload.personId;
        state.official_id = payload.officialId;
        state.person_name = payload.personName;
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
    SET_QUEUE_FOR_DISCUSSION: (state, payload) => {
        state.queue_for_discussion = payload;
    },
    SET_QUEUE_FOR_TORTURE: (state, payload) => {
        state.queue_for_torture = payload;
    },
    SET_QUEUE_FOR_PUNISHMENT: (state, payload) => {
        state.queue_for_punishment = payload;
    },
    SET_TOKEN: (state, payload) => {
        localStorage.setItem("token", payload);
        state.token = payload;
    },
    SET_ROLE: (state, payload) => {
        switch (payload) {
            case 'INQUISITOR':
                localStorage.setItem("role", 0);
                state.role = 0;
                break
            case 'BISHOP':
                localStorage.setItem("role", 1);
                state.role = 1;
                break
            case 'FISCAL':
                localStorage.setItem("role", 2);
                state.role = 2;
                break
            case 'SECULAR_AUTHORITY':
                localStorage.setItem("role", 3);
                state.role = 3;
                break
            default:
                localStorage.setItem("role", 4);
                state.role = 4;
                break
        }
    },
};

const actions = {
    INCREASE_STEP(context) {
        const inq = context.getters.CUR_INQ;
        inq.step = inq.step + 1;
        context.commit('SET_CUR_INQ', inq);
    },

    //json в формате username, password, name, surname, locality_id, birth_date, person_gender -> jwt token, role, id_person, id_official, person name
    CREATE_NEW_ACCOUNT(context, payload) {
        console.log(payload);
        return new Promise((resolve, reject) => {
            axios({ url: '/auth/signup', data: payload, method: 'POST', headers: { "Authorization": "Bearer", "Content-type": "application/json" } })
                .then(resp => {
                    if (resp.status == 200) {
                        context.commit('SET_TOKEN', resp.data.data.jwt);
                        context.commit('SET_ROLE', resp.data.data.role);
                        context.commit('SET_INITIAL_INF', resp.data.data);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })

    },

    //json в формате username, password -> jwt token, role, id_person, id_official, person name
    LOG_IN_ACCOUNT(context, payload) {
        console.log(payload);
        return new Promise((resolve, reject) => {
            axios({ url: '/auth/signin', data: payload, method: 'POST', headers: { "Authorization": "Bearer" } })
                .then(resp => {
                    if (resp.status == 200) {
                        context.commit('SET_TOKEN', resp.data.data.jwt);
                        context.commit('SET_ROLE', resp.data.data.role);
                        context.commit('SET_INITIAL_INF', resp.data.data);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // bible_id, locality_id -> id inq
    CREATE_NEW_INQ(context, payload) {
        return new Promise((resolve, reject) => {
            axios({ url: '/inquisitions/start', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_CUR_INQ', {
                            id: resp.data.data,
                            bible: payload.bibleId,
                            locality: payload.localityId,
                            step: 0
                        });
                        localStorage.setItem("step", "0");
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // по official_id определяет текущую иквизицию и возвращает инфу о ней (id, bible (id, name), locality (id, name), step).
    //step - это этап, на котором находится иквизиция (0 - только создана, 1 - процесс сбора доносов запущен, 2 - процесс сбора доносов окончен (этап формирования дел)
    // 3 - это этап, когда все дела сформированы (функция get_not_resolved_cases) ничего не возвращает, 4 - все дела закончены, инквизиционный процесс завершен)
    GET_CUR_INQ(context) {
        return new Promise((resolve, reject) => {
            const official_id = context.getters.CUR_OFFICIAL;
            axios({ url: '/inquisitions/getCurrent/' + official_id, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_CUR_INQ', {
                            id: resp.data.data.id,
                            bible: resp.data.data.bible,
                            locality: resp.data.data.locality,
                            step: resp.data.data.step
                        });
                        localStorage.setItem("step", resp.data.data.step);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // inq_id -> вызвать start_accusation_process и вернуть id
    START_ACCUSATION_PROCESS(context) {
        return new Promise((resolve, reject) => {
            const inquisitionProcessId = context.getters.CUR_INQ.id;
            console.log(inquisitionProcessId)
            axios({ url: '/accusations/start', data: { inquisitionProcessId }, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_ACCUSATION_ID', resp.data.data);
                        context.dispatch('INCREASE_STEP');
                        localStorage.setItem("step", context.getters.CUR_INQ.step);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // accusation_id -> все рекорды, относящиеся к этому процессу сбора доносов в виде массива json (см ниже в методе пример данных)
    GET_ALL_ACCUSATION_RECORDS(context) {
        return new Promise((resolve, reject) => {
            const accusation_id = context.getters.CUR_ACCUSATION;
            axios({ url: '/accusations/accusationRecords/' + accusation_id, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_ACC_TABLE_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // ничего не дается на вход -> все записи об инквизициях 
    GET_ALL_INQUISITIONS(context) {
        return new Promise((resolve, reject) => {
            axios({ url: '/inquisitions/getAllInquisitions', method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_INQ_TABLE_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // accusation_id -> вызвать finish_accusation_process, ничего не возвращать 
    FINISH_ACCUSATION_PROCESS(context) {
        return new Promise((resolve, reject) => {
            const accusationId = context.getters.CUR_ACCUSATION;
            axios({ url: '/accusations/finish', data: { accusationId }, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.dispatch('INCREASE_STEP');
                        localStorage.setItem("step", context.getters.CUR_INQ.step);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // ничего на вход -> массив инфы о всех библиях см ниже формат
    GET_ALL_BIBLES(context) {
        return new Promise((resolve, reject) => {
            axios({ url: '/bibles/', method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_BIBLE_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // ничего на вход -> массив инфы о всех местностях (locality) см ниже формат
    GET_ALL_LOCALITIES(context) {
        return new Promise((resolve, reject) => {
            axios({ url: '/localities/', method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_LOCALITY_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // на вход accusation_id -> вызвать get_not_resolved_accusation_record и вернуть результат (в формате как для GET_ALL_ACCUSATION_RECORDS)
    GET_NR_ACCUSATION_RECORDS(context) {
        const accusationId = context.getters.CUR_ACCUSATION;
        return new Promise((resolve, reject) => {
            axios({ url: '/accusations/notResolvedRecords/' + accusationId, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_ACC_NR_TABLE_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // на вход inq_id ->  вызвать generate_cases, возвращать ничего не нужно
    FINISH_RESOLVING_RECORDS(context) {
        const accusationId = context.getters.CUR_ACCUSATION;
        return new Promise((resolve, reject) => {
            axios({ url: '/accusations/generateCases', data: { accusationId }, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.dispatch('INCREASE_STEP'); ///////FIX ME точно ли ок?
                        localStorage.setItem("step", context.getters.CUR_INQ.step);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // на вход inq_id -> вернуть неразрешенные дела этой инквизиции - функция get_not_resolved_cases (формат см ниже, violation_description - это конкатенация всех согрешений челикса) понадобяться дополнительные запросы
    GET_ALL_CASES(context) {
        return new Promise((resolve, reject) => {
            const inq_id = context.getters.CUR_INQ.id;
            axios({ url: '/inquisitions/allCases/' + inq_id, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_CASES_DATA', resp.data.collection);  //////чекнуть формат
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // на вход id locality ->  вернуть массив всех людей (формат см ниже)
    GET_ALL_PEOPLE(context, payload) {
        return new Promise((resolve, reject) => {
            const locality_id = context.getters.CUR_LOCALITY;
            axios({ url: '/persons/' + locality_id, data: payload, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_PEOPLE_DATA', resp.data.collection); // FIXME concat name and surname
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    /* на вход эта инфа в виде json:
    let accused = p_accused.id;
    let bishop = bishop id;
    let informer = p_informer.id;
    let violation_place = p_cur_violation_place;
    let date_time = p_cur_date_time;
    let description = p_cur_description; 
    + inq id
    -> вызвать add_accusation_record */
    ADD_ACC_RECORD(context, payload) {
        return new Promise((resolve, reject) => {
            payload["accusationId"] = context.getters.CUR_ACCUSATION;
            payload["bishop"] = context.getters.CUR_OFFICIAL;
            axios({ url: '/accusations/add', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        ///////////FIXME добавить вызов обновления табрицы record-ов
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },

    // на вход id bible ->  вернуть массив всех commandment (вызвать функцию read_bible) (формат см ниже)
    GET_ALL_COMMANDMENTS(context, payload) {
        return new Promise((resolve, reject) => {
            const bible_id = context.getters.CUR_BIBLE;
            axios({ url: '/bibles/commandments/' + bible_id, data: payload, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_COMMANDMENTS_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // { commandments_id: Array(), record_id: 5 } -> ничего возвращать не нужно
    CONNECT_COMMANDMENT(context, payload) {
        const commandments = payload.commandments;
        return new Promise((resolve, reject) => {
            axios({ url: '/accusations/connectCommandment/' + payload.record_id, data: commandments, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // case_id -> ничего возвращать не нужно
    SEND_TO_DISCUSSION(context, payload) {
        return new Promise((resolve, reject) => {
            axios({ url: '/cases/sendToDiscussion', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // функции ниже - все реализовано в функциях sql, ищи примеры применения в script1
    // case_id, result (1 - да, 0 - нет), description -> ничего возвращать не нужно
    FINISH_DISCUSSION(context, payload) {
        return new Promise((resolve, reject) => {
            axios({ url: 'cases/finishDiscussion', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // case_id -> ничего возвращать не нужно
    SEND_TO_TORTURE(context, payload) {
        return new Promise((resolve, reject) => {
            axios({ url: '/cases/sendToTorture', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // case_id -> ничего возвращать не нужно
    MAKE_TORTURE_STEP(context, payload) {
        return new Promise((resolve, reject) => {
            axios({ url: '/cases/makeTortureStep', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // case_id, result (1 - да, 0 - нет), description -> ничего возвращать не нужно
    FINISH_TORTURE(context, payload) {
        return new Promise((resolve, reject) => {
            axios({ url: '/cases/finishTorture', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
    // inq_id -> верни массив дел у которых назначена беседа (см формат ниже)
    GET_QUEUE_FOR_DISCUTTION(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    context.commit('SET_QUEUE_FOR_DISCUSSION', resp.data);
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/
        console.log(payload);
        context.commit('SET_QUEUE_FOR_DISCUSSION', [{
            id: 1,
            accused: 'Сергей Сергеевич',
            creation_date: '2023-12-23',
            description: "jhdbf", //описание преступления (ий) - возможно нужна будет конкатенация разных доносов
            violation_description: 'бла бла бла',
        }]);
    },
    // inq_id -> верни массив дел у которых назначена пытка (см формат ниже)
    GET_QUEUE_FOR_TORTURE(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
        context.commit('SET_QUEUE_FOR_TORTURE', [{
            id: 1,
            accused: 'Сергей Сергеевич',
            creation_date: '2023-12-23',
            description: "jhdbf", //описание преступления (ий) - возможно нужна будет конкатенация разных доносов
            violation_description: 'бла бла бла',
        }]);
    },
    // inq_id -> верни массив дел у которых назначено наказание (см формат ниже)
    GET_QUEUE_FOR_PUNISHMENT(context, payload) {
        /*return new Promise((resolve, reject) => {
            axios({ url: '*********', data: payload, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    resolve(resp);
                })
                .catch(err => {
                    reject(err)
                })
        })*/ //пока заглушка
        console.log(payload);
        context.commit('SET_QUEUE_FOR_PUNISHMENT', [{
            id: 1,
            accused: 'Сергей Сергеевич',
            creation_date: '2023-12-23',
            description: "jhdbf", //описание преступления (ий) - возможно нужна будет конкатенация разных доносов
            violation_description: 'бла бла бла',
            punishment: "jfgmdfms",
            prison_name: "orejkfdjmn",
        }]);
    },
    // inq_id как параметр пути -> вызвать finish_inquisition_process, ничего не возвращать 
    FINISH_INQUISITION_PROCESS(context) {
        return new Promise((resolve, reject) => {
            const incId = context.getters.CUR_INQ.id;
            axios({ url: '/inquisitions/finish' + incId, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.dispatch('INCREASE_STEP');
                        localStorage.setItem("step", context.getters.CUR_INQ.step);
                        resolve(resp);
                    } else {
                        var err = new Error(resp.statusText);
                        err.code = resp.status;
                        reject(err);
                    }
                })
                .catch(err => {
                    reject(err)
                })
        })
    },
};
export default {
    state,
    getters,
    mutations,
    actions,
};
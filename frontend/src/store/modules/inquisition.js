import axios from 'axios';
const state = () => ({

    role: localStorage.getItem('role') || -1,
    token: localStorage.getItem('token') || '',
    cur_inq: {
        id: localStorage.getItem('cur_inq_id'), bible: localStorage.getItem("cur_inq_bible"), locality: localStorage.getItem("cur_inq_locality"), step: localStorage.getItem("cur_inq_step")
    },
    
    person_id: localStorage.getItem('person_id') || 0,
    official_id: localStorage.getItem('official_id') || 0,
    person_name: localStorage.getItem('person_name') || "",

    accusation_id: localStorage.getItem('accusation_id') || 0,
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
        localStorage.setItem("person_id", payload);
        state.official_id = payload.officialId;
        localStorage.setItem("official_id", payload);
        state.person_name = payload.personName;
        localStorage.setItem("person_name", payload);
    },

    SET_ACCUSATION_ID: (state, payload) => {
        localStorage.setItem("accusation_id", payload);
        state.accusation_id = payload;
    },

    SET_CUR_INQ: (state, payload) => {
        state.cur_inq = payload;
        localStorage.setItem("inq_id", payload.id);
        localStorage.setItem("cur_inq_id", payload.id);
        localStorage.setItem("cur_inq_bible", payload.bible);
        localStorage.setItem("cur_inq_locality", payload.locality);
        localStorage.setItem("cur_inq_step", payload.step);
    },
    SET_OFFICIAL_ID: (state, payload) => {
        localStorage.setItem("official_id", payload);
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

    SELECT_BIBLE(context, payload) {
        const inq = context.getters.CUR_INQ;
        inq.bible = payload.version;
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },
    // по official_id определяет текущую иквизицию и возвращает инфу о ней (id, bible (id, name), locality (id, name), step).
    //step - это этап, на котором находится иквизиция (0 - только создана, 1 - процесс сбора доносов запущен, 2 - процесс сбора доносов окончен (этап формирования дел)
    // 3 - это этап, когда все дела сформированы (функция get_not_resolved_cases) ничего не возвращает, 4 - все дела закончены, инквизиционный процесс завершен)
    GET_CUR_INQ(context) {
        return new Promise((resolve, reject) => {
            axios({ url: '/inquisitions/getCurrentForPerson', method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_CUR_INQ', {
                            id: resp.data.data.id,
                            bible: resp.data.data.bible,
                            locality: resp.data.data.locality,
                            step: resp.data.data.step
                        });
                        context.commit('SET_ACCUSATION_ID', resp.data.data.currentAccusationProcess);
                        console.log(context.getters.CUR_INQ);
                        localStorage.setItem("step", resp.data.data.step);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        context.dispatch('INCREASE_STEP'); ///////FIXME точно ли ок?
                        localStorage.setItem("step", context.getters.CUR_INQ.step);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },

    // на вход id bible ->  вернуть массив всех commandment (вызвать функцию read_bible) (формат см ниже)
    GET_ALL_COMMANDMENTS(context, payload) {
        return new Promise((resolve, reject) => {
            let bible_id = context.getters.CUR_BIBLE;
            if (bible_id == 0 || bible_id == undefined || bible_id == null) {
                bible_id = 1;
            }
            axios({ url: '/bibles/commandments/' + bible_id, data: payload, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_COMMANDMENTS_DATA', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },
    // { commandments_id: Array(), record_id: 5 } -> ничего возвращать не нужно
    CONNECT_COMMANDMENT(context, payload) {
        console.log(payload);
        const commandments = payload.commandments;
        const record = payload.record_id;
        return new Promise((resolve, reject) => {
            axios({ url: '/accusations/connectCommandment/' + record, data: { commandments }, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
                       var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },
    // inq_id -> верни массив дел у которых назначена беседа (см формат ниже)
    GET_QUEUE_FOR_DISCUTTION(context, payload) {
        return new Promise((resolve, reject) => {
            console.log(payload);
            const inq_id = context.getters.CUR_INQ.id;
            axios({ url: '/cases/forDiscussion/' + inq_id, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_QUEUE_FOR_DISCUSSION', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },
    // inq_id -> верни массив дел у которых назначена пытка (см формат ниже)
    GET_QUEUE_FOR_TORTURE(context, payload) {
        return new Promise((resolve, reject) => {
            console.log(payload);
            const inq_id = context.getters.CUR_INQ.id;
            axios({ url: '/cases/forTorture/' + inq_id, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_QUEUE_FOR_TORTURE', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },
    // inq_id -> верни массив дел у которых назначено наказание (см формат ниже)
    GET_QUEUE_FOR_PUNISHMENT(context, payload) {
        return new Promise((resolve, reject) => {
            console.log(payload);
            const inq_id = context.getters.CUR_INQ.id;
            axios({ url: '/cases/forPunishment/' + inq_id, method: 'GET', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.commit('SET_QUEUE_FOR_PUNISHMENT', resp.data.collection);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
                })
        })
    },
    // inq_id как параметр пути -> вызвать finish_inquisition_process, ничего не возвращать 
    FINISH_INQUISITION_PROCESS(context) {
        return new Promise((resolve, reject) => {
            const inquisitionId = context.getters.CUR_INQ.id;
            axios({ url: '/inquisitions/finish', data: { inquisitionId }, method: 'POST', headers: { "Authorization": "Bearer " + localStorage.getItem("token") } })
                .then(resp => {
                    console.log(resp);
                    if (resp.status == 200) {
                        context.dispatch('INCREASE_STEP');
                        localStorage.setItem("step", context.getters.CUR_INQ.step);
                        resolve(resp);
                    } else {
                        var err = { message: resp.message };
                        reject(err);
                    }
                })
                .catch(error => {
                    var err = error.response.data;
                    reject(err);
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
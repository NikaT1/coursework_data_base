//import axios from 'axios';
const state = () => ({
	cur_inq: null,
	token: localStorage.getItem('token') || '',
	person_id: 0,
	official_id: 0,
	accusation_id: 0,
	inq_table_data: [],
	acc_table_data: [],
	acc_nr_table_data: [],
	cases_data: [],
	locality_data: [],
	bible_data: []
});
const getters = {
	CUR_INQ: state => {
		return state.cur_inq;
	},
	CUR_OFFICIAL: state => {
		return state.official_id;
	},
};
const mutations = {
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
};

const actions = {
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
					resolve(resp);
				})
				.catch(err => {
					reject(err)
				})
		})*/  //пока заглушка
		context.commit('SET_CUR_INQ', {
			id: 1,
			bible: payload.bible,
			locality: payload.locality,
			step: 0
		});

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
			step: 0
		});
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
			informer: 'Виктор Викторович',
			bishop: 'Виктор Викторович',
			accused: 'Сергей Сергеевич',
			violation_place: 'дома',
			date_time: '2023-12-23',
			description: 'бла бла бля',
		}]);
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
		context.commit('SET_ACC_NR_TABLE_DATA', [{
			informer: 'Виктор Викторович',
			bishop: 'Виктор Викторович',
			accused: 'Сергей Сергеевич',
			violation_place: 'дома',
			date_time: '2023-12-23',
			description: 'бла бла бля',
		}]);
	},
	// на вход inq_id -> вызвать finish_accusation_proccess, generate_cases и вернуть результат (формат см ниже, violation_description - это конкатенация всех согрешений челикса)
	GET_ALL_CASES(context, payload) {
		/*return new Promise((resolve, reject) => {
			axios({ url: '*********', data: payload, method: 'GET' })
				.then(resp => {
					context.commit('SET_CASES_DATA', resp.data);
					resolve(resp);
				})
				.catch(err => {
					reject(err)
				})
		})*/ //пока заглушка
		console.log(payload);
		context.commit('SET_CASES_DATA', [{
			id: 1,
			accused: 'Сергей Сергеевич',
			creation_date: '2023-12-23',
			violation_description: 'бла бла бля',
		}]);
	},
};
export default {
	state,
	getters,
	mutations,
	actions,
};
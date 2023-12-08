import axios from 'axios';
const state = () => ({
	role: -1,
	token: localStorage.getItem('token') || '',
});
const getters = {
	CUR_ROLE: state => {
		return state.role;
	},
	CUR_TOKEN: state => {
		return state.token;
	},
};
const mutations = {
	SET_TOKEN: (state, payload) => {
		state.token = payload;
	},
	SET_ROLE: (state, payload) => {
		state.role = payload;
	},
};

const actions = {
	//json в формате role, login, password, name, surname, locality_id, birth_date, person_gender -> jwt token
	CREATE_NEW_ACCOUNT(context, payload) {
		return new Promise((resolve, reject) => {
			axios({ url: '/api/auth/signin', data: payload, method: 'POST' })
				.then(resp => {
					context.commit('SET_TOKEN', resp.data.token);
					context.commit('SET_ROLE', payload.role);
					resolve(resp);
				})
				.catch(err => {
					reject(err)
				})
		})

	},

	//json в формате login, password -> jwt token, role
	LOG_IN_ACCOUNT(context, payload) {
		return new Promise((resolve, reject) => {
			axios({ url: '/api/auth/signin', data: payload, method: 'POST' })
				.then(resp => {
					context.commit('SET_TOKEN', resp.data.token);
					context.commit('SET_ROLE', payload.role);
					resolve(resp);
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
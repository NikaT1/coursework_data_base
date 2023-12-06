//import axios from 'axios';
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
	CREATE_NEW_ACCOUNT(context, payload) {
		/*return new Promise((resolve, reject) => {
			axios({ url: '*********', data: payload, method: 'POST' })
				.then(resp => {
					context.commit('SET_TOKEN', resp.data.token);
					context.commit('SET_ROLE', resp.data.role);
					resolve(resp);
				})
				.catch(err => {
					reject(err)
				})
		})*/  //пока заглушка
		console.log(payload);
		context.commit('SET_TOKEN', "sjfs");
		context.commit('SET_ROLE', 0);

	},
	LOG_IN_ACCOUNT(context, payload) {
		/*return new Promise((resolve, reject) => {
			axios({ url: '*********', data: payload, method: 'GET' })
				.then(resp => {
					context.commit('SET_TOKEN', resp.data.token);
					context.commit('SET_ROLE', resp.data.role);
					resolve(resp);
				})
				.catch(err => {
					reject(err)
				})
		})*/  //пока заглушка
		console.log(payload);
		context.commit('SET_TOKEN', "sjfs");
		context.commit('SET_ROLE', 0);

	},

};
export default {
	state,
	getters,
	mutations,
	actions,
};
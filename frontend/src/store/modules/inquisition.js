import axios from 'axios';
const state = {
	cur_inq: null,
	token: localStorage.getItem('token') || '',
};
const getters = {
	CUR_INQ: state => {
		return state.cur_inq;
	}
};
const mutations = {
	SET_CUR_INQ: (state, payload) => {
		state.cur_inq = payload;
	},
};

const actions = {
	CREATE_NEW_INQ(context, inq_data) {
		alert(inq_data);
		return new Promise((resolve, reject) => {
			axios({ url: '*********', data: inq_data, method: 'POST' })
				.then(resp => {
					context.commit('SET_CUR_INQ_ID', {
						id: resp.data.id,
						bible: inq_data.bible,
						locality: inq_data.locality
					});
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
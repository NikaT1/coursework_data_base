import inquisition from './modules/inquisition.js';
import accounts from './modules/accounts.js';
import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
    modules: {
        inquisition,
        accounts,
    }
})

export default store;
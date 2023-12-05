import inquisition from './modules/inquisition.js';
import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
    modules: {
        inquisition: inquisition,
    }
})

export default store;
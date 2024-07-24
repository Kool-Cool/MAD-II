import { createStore } from 'vuex';

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    logout(state) {
      state.token = '';
      localStorage.removeItem('token');
    },
  },
  actions: {
    logout({ commit }) {
      commit('logout');
    },
  },
  getters: {
    isAuthenticated: state => !!state.token,
  },
});

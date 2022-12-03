export default {
  state: () => ({
    config: {},
  }),
  mutations: {
    setConfig(state, item) {
      for (let key of Object.keys(item)) {
        state.config[key] = item[key].strategy;
      }
    },
  }
}
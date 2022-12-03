export default {
  state: () => ({
    userItem: {},
    warehouseItems: [],
    currentWarehouse: undefined,
  }),
  mutations: {
    setUserItem(state, data) {
      state.userItem = data;
    },
    setWarehouseItems(state, data) {
      state.warehouseItems = data;
    },
    setCurrentWarehouse(state, data) {
      state.currentWarehouse = data;
    },
  }
}

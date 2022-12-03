export default {
  state: () => ({
    username: '',
    isManager: false,
    permissions: [],
    config: {},
    barConfig: {},
    currentWarehouse: undefined,
  }),
  mutations: {
    setUser(state, item) {
      state.username = item.username;
      state.isManager = item.is_manager;
      state.permissions = item.permissions;
      state.barConfig = {
        batchLabelLength: item.batch_label_length,
        batchLabelWidth: item.batch_label_width,
        locationLabelLength: item.location_label_length,
        locationLabelWidth: item.location_label_width,
        materialLabelLength: item.material_label_length,
        materialLabelWidth: item.material_label_width,
        palletLabelLength: item.pallet_label_length,
        palletLabelWidth: item.pallet_label_width,
      }
      if (item.configs) {
        for (let config of item.configs) {
          state.config[config.type] = config.strategy;
        }
      }
    },
    setWarehouse(state, value) {
      state.currentWarehouse = value;
    },
    setBarConfig(state, value) {
      state.barConfig = {
        batchLabelLength: value.batch_label_length,
        batchLabelWidth: value.batch_label_width,
        locationLabelLength: value.location_label_length,
        locationLabelWidth: value.location_label_width,
        materialLabelLength: value.material_label_length,
        materialLabelWidth: value.material_label_width,
        palletLabelLength: value.pallet_label_length,
        palletLabelWidth: value.pallet_label_width,
      }
    },
  }
}
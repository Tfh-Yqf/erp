<template>
  <div>
    <a-row gutter="12">
      <a-col :span="24">
        <a-select v-model="batch" placeholder="批次" :loading="batchLoading" :disabled="batchLoading"
          style="width: 100%;" @change="onChangeBatch">
          <a-select-option v-for="item in batchItems" :key="item.id" :value="item.id">
            {{ item.number }}
          </a-select-option>
        </a-select>
      </a-col>
      <a-col :span="24">
        <a-select v-model="shelveRecord" placeholder="上架记录" :loading="shelveRecordLoading" :disabled="shelveRecordLoading"
          style="width: 100%;" @change="onChangeShelveRecord">
          <a-select-option v-for="item in shelveRecordItems" :key="item.id" :value="item.id">
            {{ item.warehouse_name }} - {{item.location_number}}: {{item.remain_quantity}}
          </a-select-option>
        </a-select>
      </a-col>
    </a-row>
  </div>
</template>

<script>
  import { batchOption, shelveRecordOption } from '@/api/option';

  export default {
    props: ['shelveRecord', 'material'],
    model: { prop: 'shelveRecord', event: 'change' },
    data() {
      return {
        batchItems: [],
        shelveRecordItems: [],
        batchLoading: false,
        shelveRecordLoading: false,
        batch: undefined,
      }
    },
    methods: {
      initData() {
        this.batchLoading = true;
        batchOption({ page_size: 999999, material: this.material }).then(data => {
          this.batchItems = data.results;
          if (this.batchItems.length > 0) {
            this.batch = this.batchItems[0].id;
            this.onChangeBatch();
          }
        }).finally(() => {
          this.batchLoading = false;
        });
      },
      onChangeBatch() {
        this.shelveRecordLoading = true;
        shelveRecordOption({ page_size: 999999, batch: this.batch }).then(data => {
          this.shelveRecordItems = data.results;
          if (this.shelveRecordItems.length > 0) {
            this.onChangeShelveRecord(this.shelveRecordItems[0].id);
          }
        }).finally(() => {
          this.shelveRecordLoading = false;
        });
      },
      onChangeShelveRecord(value) {
        this.$emit('change', value);
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
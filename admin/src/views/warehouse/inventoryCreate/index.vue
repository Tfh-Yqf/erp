<template>
  <div>
    <a-card title="盘点单">
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <a-spin :spinning="loading">
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="number" label="调拨编号">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="warehouse" label="仓库">
                <a-select v-model="form.warehouse" style="width: 100%" @change="changeWarehouse">
                  <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="handler" label="经手人">
                <a-select v-model="form.handler" style="width: 100%">
                  <a-select-option v-for="item in handlerItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="handle_time" label="处理日期">
                <a-date-picker v-model="form.handle_time" valueFormat="YYYY-MM-DD" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="remark" label="备注">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>

        <div>
          <a-row gutter="16">
            <a-space>
              <a-button type="primary" @click="openMaterialModal">添加产品</a-button>
            </a-space>
          </a-row>
          <div style="margin-top: 16px;">
              <a-table rowKey="id" size="middle" :columns="columns" :data-source="goodsData"
                :pagination="false">
                <div slot="actual_quantity" slot-scope="value, item, index">
                  <div v-if="!!item.enable_batch_control">
                    <div v-if="item.isTotal">{{ value }}</div>
                    <div v-else>
                      <a-input :value="item.actual_quantity" disabled style="width:75%;" />
                      <a-button @click="chooseBatch(item, index)">批</a-button>
                    </div>
                  </div>
                  <div v-else>
                    <div v-if="item.isTotal">{{ value }}</div>
                    <a-input-number v-else v-model="item.actual_quantity" :min="0" size="small"></a-input-number>
                  </div>
                </div>
                <div slot="action" slot-scope="value, item, index">
                  <a-button-group v-if="!item.isTotal" size="small">
                    <a-button type="danger" @click="removeMaterial(item)">移除</a-button>
                  </a-button-group>
                </div>
              </a-table>
          </div>
        </div>
      </a-spin>

      <div style="margin-top: 32px;">
        <a-popconfirm title="确定创建吗?" @confirm="create">
          <a-button type="primary" :loading="loading">创建</a-button>
        </a-popconfirm>
      </div>
    </a-card>
    <materials-select-modal v-model="materialsSelectModalVisible" :warehouse="form.warehouse" @select="onSelectMaterial"></materials-select-modal>
    <!-- 批次 -->
    <a-modal
      :title="batchTitle"
      v-model="batchVisible"
      width="750px"
      cancelText="关闭"
      :maskClosable="false"
      @cancel="batchVisible=false"
      @ok="confirmChoosed">
      <div style="margin-bottom: 16px">
        <a-button type="primary" icon="plus" style="margin: 0 8px;" @click="addLine">添加</a-button>
      </div>
      <a-table
        rowkey="id"
        :columns="columnsBatch"
        :data-source="stockCheckBatchItems"
        :pagination="false"
        style="width: 100%" >
        <div slot="actual_quantity" slot-scope="value, item">
          <a-input-number
            :value="item.actual_quantity"
            min="1"
            @change="(value) => changeQuantityBatch(value, item, 'actual_quantity')" />
        </div>
        <div slot="batch_number" slot-scope="value, item">
          <a-select v-model="item.batch_number" @change="(e) => changeQuantityBatch(e, item, 'batch_number')" style="width: 100%">
            <a-select-option v-for="Batch in curBatchOptions" :key="Batch.number" :value="Batch.number">
              {{ Batch.number }}
            </a-select-option>
          </a-select>
        </div>
        <div slot="production_date" slot-scope="value, item">
          <a-date-picker
            :value="item.production_date"
            valueFormat="YYYY-MM-DD"
            @change="(value) => changeQuantityBatch(value, item, 'production_date')" />
        </div>
        <div slot="action" slot-scope="value,item">
          <a-button icon="minus" @click="removeLine(item)"></a-button>
        </div>
      </a-table>
    </a-modal>
  </div>
</template>

<script>
  import moment from 'moment';
  import { getStockCheckOrderNumber } from '@/api/data'
  import { stockCheckCreate } from '@/api/warehouse';
  import { userOption, warehousesOption, inventoriesOption, batchsOption } from '@/api/option'
  import NP from 'number-precision'

  export default {
    components: {
      MaterialsSelectModal: () => import('@/components/MaterialSelectModal/index'),
    },
    data() {
      return {
        description: '新增',
        batchTitle: '',
        warehouseItems: [],
        handlerItems: [],
        materialsSelectModalVisible: false,
        batchVisible: false,
        loading: false,
        model: {},
        form: {},
        rules: {
          number: [
            { required: true, message: '请输入编号', trigger: 'change' },
          ],
          warehouse: [
            { required: true, message: '请选择仓库', trigger: 'change' }
          ],
          handler: [
            { required: true, message: '请选择经手人', trigger: 'change' }
          ],
          handle_time: [
            { required: true, message: '请选择处理日期', trigger: 'change' },
          ],
        },
        columns: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            width: 45,
            customRender: (value, item, index) => {
              return item.isTotal ? '合计' : (index + 1)
            },
          },
          {
            title: '名称',
            dataIndex: 'name',
            key: 'name',
            width: 150,
          },
          {
            title: '编号',
            dataIndex: 'number',
            key: 'number',
            width: 150,
          },
          {
            title: '规格',
            dataIndex: 'spec',
            key: 'spec',
            width: 150,
          },
          {
            title: '单位',
            dataIndex: 'unit',
            key: 'unit',
            width: 80,
          },
          {
            title: '批次控制',
            dataIndex: 'enable_batch_control',
            key: 'enable_batch_control',
            width: 80,
            customRender: (value, item, index) => {
              return item.isTotal ? '合计' : (item.enable_batch_control ? '开启' :'未开启')
            },
          },
          {
            title: '实际数量',
            dataIndex: 'actual_quantity',
            key: 'actual_quantity',
            width: 180,
            scopedSlots: { customRender: 'actual_quantity' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            width: 80,
            scopedSlots: { customRender: 'action' },
          },
        ],
        materialItems: [],
        columnsBatch: [
          {
            title: '序号',
            dataIndex: 'index',
            key: 'index',
            customRender: (value, item, index) => {
              return index + 1
            },
          },
          {
            title: "编号",
            dataIndex: "batch_number",
            key: "batch_number",
            scopedSlots: { customRender: "batch_number" },
          },
          {
            title: "实际数量",
            dataIndex: "actual_quantity",
            key: "actual_quantity",
            scopedSlots: { customRender: "actual_quantity" },
          },
          {
            title: "生产日期",
            dataIndex: "production_date",
            key: "production_date",
            scopedSlots: { customRender: "production_date" },
          },
          {
            title: '操作',
            dataIndex: 'action',
            scopedSlots: { customRender: 'action' },
            width: '80px'
          },
        ],
        curBatchOptions: {},
        curGoodsLineIdx: null,
        stockCheckBatchItems: []
      }
    },
    computed: {
      goodsData() {
        // 统计合计
        let totalQuantity = 0,
          totalAmount = 0;
        for (let item of this.materialItems) {
          totalQuantity = NP.plus(totalQuantity, item.actual_quantity);
        }
        return [
          ...this.materialItems,
          {
            id: '-1',
            isTotal: true,
            name: '',
            actual_quantity: totalQuantity,
          },
        ];
      },
    },
    methods: {
      moment,
      initData() {
        this.resetForm();
        warehousesOption({ page_size: 999999, is_active: true }).then(data => {
          this.warehouseItems = data.results;
        });
        userOption({ page_size: 999999, is_active: true }).then(data => {
          this.handlerItems = data.results;
        });
      },
      changeWarehouse() {
        this.materialItems = [];
      },
      openMaterialModal() {
        if (!this.form.warehouse) {
          this.$message.warn('请先选择仓库！');
          return false;
        }
        this.materialsSelectModalVisible = true;
      },
      async onSelectMaterial(item) {
        let index = this.materialItems.findIndex(_item => _item.id == item.id);
        if (index != -1) {
          this.$message.warn('产品已存在');
          return
        }
        let batchOptions = await batchsOption({ page_size: 999999, warehouse: this.form.warehouse, goods: item.goods  }).then(data => {
          return data.results;
        })
        this.materialItems = this.$functions.insertItem(this.materialItems, {
          id: item.id,
          goods: item.goods,
          number: item.goods_number,
          name: item.goods_name,
          spec: item.goods_spec,
          unit: item.unit_name,
          actual_quantity: 1,
          enable_batch_control: item.enable_batch_control,
          batchOptions: batchOptions,
          stock_check_batch_items: []
        });
      },
      removeMaterial(item) {
        this.materialItems = this.$functions.removeItem(this.materialItems, item);
      },
      chooseBatch(item, index) {
        console.log(item, index)
        this.batchTitle = '管理批次';
        this.curBatchOptions = item.batchOptions;
        this.curGoodsLineIdx = index;
        if (item.stock_check_batch_items.length) {
          this.stockCheckBatchItems = item.stock_check_batch_items;
        } else {
          this.stockCheckBatchItems = [
            {
              key: 'uni1',
              batch_number: '',
              actual_quantity: 1,
              production_date: null
            }
          ];
        }
        this.batchVisible = true;
      },
      confirmChoosed() {
        let ifHasEmpty = false;
        let sumAmount = 0;
        this.stockCheckBatchItems.map(item => {
          sumAmount+=item.actual_quantity
          if (!item.batch_number || !item.actual_quantity) {
            ifHasEmpty = true;
          }
        })
        if (ifHasEmpty) {
          this.$message.warn('请将批次信息填写完整!');
          return
        }
        let tmp = {...this.materialItems[this.curGoodsLineIdx], ...{ stock_check_batch_items: this.stockCheckBatchItems, actual_quantity: sumAmount }}
        this.materialItems = this.$functions.replaceItem(this.materialItems, tmp);
        this.batchVisible = false;
      },
      addLine() {
        const { stockCheckBatchItems } = this;
        const newData = {
          key: 'uni' + stockCheckBatchItems.length + 1,
          batch_number: '',
          actual_quantity: 1,
          production_date: null
        };
        this.stockCheckBatchItems = [...stockCheckBatchItems, newData];
      },
      removeLine(item) {
        this.stockCheckBatchItems = this.$functions.removeItemBatch(this.stockCheckBatchItems, item);
      },
      changeQuantity(value, item) {
        item['actual_quantity'] = value || 0;
        // this.warehouseItems = this.$functions.replaceItem(this.warehouseItems, item);
      },
      changeQuantityBatch(e, item, pro) {
        item[pro] = e;
        // if (pro === 'actual_quantity') {
        //   item[pro] = e;
        // } else {
        //   let tmp = e.split('|');
        //   item[pro] = tmp[1];
        //   item['batch'] = tmp[0];
        // }
        this.stockCheckBatchItems[item.key - 1] = item;
      },
      create() {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
             let ifHasEmptyGoods = false;
             let ifHasEmptyBatch = false;
            if (this.materialItems.length == 0) {
              this.$message.warn('未添加产品');
              return false
            }
            this.materialItems.map(item => {
              if (!item.actual_quantity) {
                ifHasEmptyGoods = true;
              }
              if (item.enable_batch_control && !item.stock_check_batch_items.length) {
                ifHasEmptyBatch = true;
              }
            })
            if (ifHasEmptyGoods) {
              this.$message.warn('实际数量必填');
              return false
            }
            if (ifHasEmptyBatch) {
              this.$message.warn('开启批次控制的产品, 需要完善该产品的批次信息');
              return false
            }
            this.loading = true;
            let formData = {
              ...this.form,
              stock_check_goods_Items: this.materialItems.map(item => {
                return {
                  goods: item.goods,
                  actual_quantity: item.actual_quantity,
                  stock_check_batch_items: item.stock_check_batch_items
                }
              })
            };
            console.log(formData)
            stockCheckCreate(formData).then(data => {
              this.$message.success('创建成功');
              this.$router.push({ path: '/warehouse/inventory' });
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      resetForm() {
        this.form = {};
        getStockCheckOrderNumber().then(data => {
          this.form = { number: data.number }
        })
        this.materialItems = [];
      },
    },
    mounted() {
      this.initData();
    }
  }
</script>
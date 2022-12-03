<template>
  <div>
    <a-card title="调拨">
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
              <a-form-model-item prop="out_warehouse" label="出库仓库">
                <a-select v-model="form.out_warehouse" style="width: 100%">
                  <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="in_warehouse" label="入库仓库">
                <a-select v-model="form.in_warehouse" style="width: 100%">
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
                <div slot="stock_transfer_quantity" slot-scope="value, item, index">
                  <div v-if="item.isTotal">{{ value }}</div>
                  <a-input-number v-else v-model="item.stock_transfer_quantity" :min="0" size="small"></a-input-number>
                </div>
                <div slot="batch" slot-scope="value, item, index">
                  <a-select v-if="!item.isTotal" v-model="item.batch" style="width: 100%">
                    <a-select-option v-for="item in item.batchItems" :key="item.id" :value="item.id">
                      {{ item.number }}
                    </a-select-option>
                  </a-select>
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
    <materials-select-modal v-model="materialsSelectModalVisible" :warehouse="form.out_warehouse" @select="onSelectMaterial"></materials-select-modal>
  </div>
</template>

<script>
  import moment from 'moment';
  import { getStockTransferOrderNumber } from '@/api/data'
  import { stockTransferCreate } from '@/api/warehouse';
  import { userOption, warehousesOption, inventoriesOption, batchsOption } from '@/api/option'
  import NP from 'number-precision'

  export default {
    components: {
      MaterialsSelectModal: () => import('@/components/MaterialSelectModal/index'),
    },
    data() {
      return {
        description: '新增',
        warehouseItems: [],
        handlerItems: [],
        materialsSelectModalVisible: false,
        loading: false,
        model: {},
        form: {},
        rules: {
          number: [
            { required: true, message: '请输入编号', trigger: 'change' },
          ],
          out_warehouse: [
            { required: true, message: '请选择出库仓库', trigger: 'change' }
          ],
          in_warehouse: [
            { required: true, message: '请选择入库仓库', trigger: 'change' }
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
            title: '调拨数量',
            dataIndex: 'stock_transfer_quantity',
            key: 'stock_transfer_quantity',
            width: 120,
            scopedSlots: { customRender: 'stock_transfer_quantity' },
          },
          // {
          //   title: '批次',
          //   dataIndex: 'batch',
          //   key: 'batch',
          //   width: 120,
          //   scopedSlots: { customRender: 'batch' },
          // },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            width: 80,
            scopedSlots: { customRender: 'action' },
          },
        ],
        materialItems: [],
      }
    },
    computed: {
      goodsData() {
        // 统计合计
        let totalQuantity = 0,
          totalAmount = 0;
        for (let item of this.materialItems) {
          totalQuantity = NP.plus(totalQuantity, item.stock_transfer_quantity);
        }
        return [
          ...this.materialItems,
          {
            id: '-1',
            isTotal: true,
            name: '',
            stock_transfer_quantity: totalQuantity,
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
      openMaterialModal() {
        if (!this.form.out_warehouse) {
          this.$message.warn('请先选择出库仓库！');
          return false;
        }
        this.materialsSelectModalVisible = true;
      },
      onSelectMaterial(item) {
        let index = this.materialItems.findIndex(_item => _item.id == item.id);
        if (index != -1) {
          this.$message.warn('产品已存在');
          return
        }
        this.materialItems = this.$functions.insertItem(this.materialItems, {
          id: item.id,
          goods: item.goods,
          number: item.goods_number,
          name: item.goods_name,
          spec: item.goods_spec,
          unit: item.unit_name,
          stock_transfer_quantity: 1,
          // batch: '',
          // batchsItem: batchsOption({ page_size: 999999, warehouse: this.form.out_warehouse, goods: item.id  }).then(data => {
          //   return data.results;
          // })
        });
      },
      removeMaterial(item) {
        this.materialItems = this.$functions.removeItem(this.materialItems, item);
      },
      create() {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
             let ifHasEmptyGoods = false;
            if (this.materialItems.length == 0) {
              this.$message.warn('未添加产品');
              return false
            }
            this.materialItems.map(item => {
              if (!item.stock_transfer_quantity) {
                ifHasEmptyGoods = true;
              }
            })
            if (ifHasEmptyGoods) {
              this.$message.warn('调拨数量必填');
              return false
            }
            this.loading = true;
            let formData = {
              ...this.form,
              stock_transfer_goods_items: this.materialItems.map(item => {
                return {
                  goods: item.goods,
                  stock_transfer_quantity: item.stock_transfer_quantity,
                }
              })
            };
            stockTransferCreate(formData).then(data => {
              this.$message.success('创建成功');
              this.$router.push({ path: '/warehouse/allocation' });
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      resetForm() {
        this.form = {};
        getStockTransferOrderNumber().then(data => {
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
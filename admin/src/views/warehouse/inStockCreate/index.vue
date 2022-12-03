<template>
  <div>
    <a-card title="入库创建">
      <a-button slot="extra" type="primary" ghost @click="() => { this.$router.go(-1); }"> <a-icon type="left" />返回</a-button>
      <section>
        <a-spin :spinning="loading">
          <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 7 }" :wrapper-col="{ span: 16 }">
            <a-row>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="number" label="编号">
                  {{ info.number }}
                </a-form-model-item>
              </a-col>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="warehouse_name" label="仓库">
                  {{ info.warehouse_name }}
                </a-form-model-item>
              </a-col>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="type_display" label="入库类型">
                  {{ info.type_display }}
                </a-form-model-item>
              </a-col>
              <a-col :span="6" style="width: 320px;">
                <a-form-model-item prop="" :label="info.type === 'purchase' ? '采购单据' : (info.type === 'sales_return' ? '销售退货单据' : '调拨单据')">
                  {{ info.type === 'purchase' ? info.purchase_order_number : (info.type === 'sales_return' ? info.sales_return_order_number : info.stock_transfer_order_number) }}
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
            <a-table rowKey="id" size="middle" :columns="columns" :data-source="goodsData" :pagination="false">
              <div slot="stock_in_quantity" slot-scope="value, item, index">
                <div v-if="item.isTotal">{{ value }}</div>
                <a-input-number v-else v-model="item.stock_in_quantity" :min="0" size="small"></a-input-number>
              </div>
              <div slot="batch_number" slot-scope="value, item, index">
                <a-input v-if="!item.isTotal" v-model="item.batch_number" size="small"></a-input>
              </div>
              <div slot="production_date" slot-scope="value, item, index">
                <a-date-picker v-if="!item.isTotal" v-model="item.production_date" valueFormat="YYYY-MM-DD" style="width: 100%" />
              </div>
              <!-- <div slot="action" slot-scope="value, item, index">
                <a-button-group v-if="!item.isTotal" size="small">
                  <a-button type="danger" @click="removeMaterial(item)">移除</a-button>
                </a-button-group>
              </div> -->
            </a-table>
          </a-form-model>
        </a-spin>
        <div style="margin-top: 32px;">
          <a-popconfirm title="确定创建吗?" @confirm="create">
            <a-button type="primary" :loading="loading">创建</a-button>
          </a-popconfirm>
        </div>
      </section>
    </a-card>
  </div>
</template>

<script>
  import { userOption, warehousesOption } from '@/api/option'
  import { stockInOrderDetail, stockInCreate } from '@/api/warehouse'
  import NP from 'number-precision'

  export default {
    data() {
      return {
        loading: true,
        info: {},
        form: {},
        rules: {
          // name: [{ required: true, message: '请输入名称', trigger: 'change' }],
          // number: [{ required: true, message: '请输入编号', trigger: 'change' }],
          // initial_arrears_amount: [
          //   { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '初期欠款金额格式不正确', trigger: 'change' }
          // ],
        },
        warehouseItems: [],
        handlerItems: [],
        materialItems: [],
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
            dataIndex: 'goods_name',
            key: 'goods_name',
            width: 150,
          },
          {
            title: '编号',
            dataIndex: 'goods_number',
            key: 'goods_number',
            width: 150,
          },
          {
            title: '入库数量',
            dataIndex: 'stock_in_quantity',
            key: 'stock_in_quantity',
            width: 120,
            scopedSlots: { customRender: 'stock_in_quantity' },
          },
          {
            title: '单位',
            dataIndex: 'unit_name',
            key: 'unit_name',
            width: 80,
          },
          {
            title: '批次控制',
            dataIndex: 'enable_batch_control',
            key: 'enable_batch_control',
            width: 80,
            customRender: (value, item, index) => {
              return item.isTotal ? '' : (value ? '已开启' : '未开启')
            },
          },
          {
            title: '批次',
            dataIndex: 'batch_number',
            key: 'batch_number',
            width: 120,
            scopedSlots: { customRender: 'batch_number' },
          },
          {
            title: '生产日期',
            dataIndex: 'production_date',
            key: 'production_date',
            width: 150,
            scopedSlots: { customRender: 'production_date' },
          },
          {
            title: '保质期天数',
            dataIndex: 'shelf_life_days',
            key: 'shelf_life_days',
            width: 120,
          },
          // {
          //   title: '操作',
          //   dataIndex: 'action',
          //   key: 'action',
          //   width: 80,
          //   scopedSlots: { customRender: 'action' },
          // },
        ],
      }
    },
    created(){
      this.initData();
    },
    computed: {
      goodsData() {
        // 统计合计
        let totalQuantity = 0,
          totalAmount = 0;
        for (let item of this.materialItems) {
          totalQuantity = NP.plus(totalQuantity, item.stock_in_quantity);
        }
        return [
          ...this.materialItems,
          {
            id: '-1',
            isTotal: true,
            name: '',
            stock_in_quantity: totalQuantity,
          },
        ];
      },
    },
    methods: {
      initData() {
        warehousesOption({ page_size: 999999, is_active: true }).then(data => {
          this.warehouseItems = data.results;
        });
        userOption({ page_size: 999999, is_active: true }).then(data => {
          this.handlerItems = data.results;
        });
        stockInOrderDetail({ id: this.$route.query.id }).then(data => {
          this.info = data;
          this.materialItems = data.stock_in_goods_items;
        }).finally(() => {
          this.loading = false;
        });
      },
      create() {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            let ifHasEmptyBatch = false;
            let ifHasEmptyAmount = false;
            this.materialItems.map(item => {
              if (item.enable_batch_control && !item.batch_number) {
                ifHasEmptyBatch = true;
              }
              if (!item.stock_in_quantity) {
                ifHasEmptyAmount = true;
              }
            })
            if (ifHasEmptyAmount) {
              this.$message.warn('请输入入库数量');
              return false
            }
            if (ifHasEmptyBatch) {
              this.$message.warn('开启批次控制的产品需要输入批次编号');
              return false
            }

            // this.loading = true;
            let formData = {
              ...this.form,
              stock_in_order: this.info.id,
              stock_in_record_goods_items: this.materialItems.map(item => {
                return {
                  stock_in_goods: item.id,
                  stock_in_quantity: item.stock_in_quantity,
                  batch_number: item.batch_number,
                  production_date: item.production_date,
                }
              })
            };
            stockInCreate(formData).then(data => {
              this.$message.success('创建成功');
              this.$router.push({ path: '/warehouse/inStock'});
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
    },
    mounted() {
      this.initData();
    },
  }
</script>
<style>
</style>

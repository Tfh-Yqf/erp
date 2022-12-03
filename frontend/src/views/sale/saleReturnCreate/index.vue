<template>
  <div>
    <a-card title="销售退货单">
      <a-spin :spinning="loading">
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="number" label="销售编号">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="sales_order" label="销售单据">
                <a-select v-model="form.sales_order" @change="changeRelatedOrder" style="width: 100%">
                  <a-select-option v-for="item in saleOrdersItems" :key="item.id" :value="item.id">
                    {{ item.number }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="warehouse" label="仓库">
                <a-select v-model="form.warehouse" style="width: 100%">
                  <a-select-option v-for="item in warehouseItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="client" label="客户">
                <a-select v-model="form.client" style="width: 100%">
                  <a-select-option v-for="item in clientsItems" :key="item.id" :value="item.id">
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
            <!-- <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="discount" label="整单折扣">
                <a-input-number v-model="form.discount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="other_amount" label="其他费用">
                <a-input-number v-model="form.other_amount" style="width: 100%;" />
              </a-form-model-item>
            </a-col> -->
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="remark" label="备注">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
          </a-row>
        </a-form-model>

        <a-divider orientation="left">产品信息</a-divider>

        <div>
          <a-row gutter="16">
            <a-space>
              <a-button type="primary" @click="openMaterialModal">添加产品</a-button>
            </a-space>
          </a-row>
          <div style="margin-top: 16px;">
              <a-table rowKey="id" size="middle" :columns="columns" :data-source="goodsData"
                :pagination="false">
                <div slot="return_quantity" slot-scope="value, item, index">
                  <div v-if="item.isTotal">{{ value }}</div>
                  <a-input-number v-else v-model="item.return_quantity" :min="0" size="small"></a-input-number>
                </div>
                <div slot="return_price" slot-scope="value, item, index">
                  <a-input-number v-if="!item.isTotal" v-model="item.return_price" :min="0" size="small"></a-input-number>
                </div>
                <div slot="action" slot-scope="value, item, index">
                  <a-button-group v-if="!item.isTotal" size="small">
                    <a-button type="danger" @click="removeMaterial(item)">移除</a-button>
                  </a-button-group>
                </div>
              </a-table>
          </div>
        </div>

        <a-divider orientation="left">账单信息</a-divider>
        <div>
          <a-row gutter="16">
            <a-col :span="4">
              <a-form-model-item prop="discount" label="整单折扣" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number v-model="form.discount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>

            <a-col :span="4">
              <a-form-model-item
                prop="other_amount"
                label="其他费用"
                :label-col="{ span: 24 }"
                :wrapper-col="{ span: 24 }"
              >
                <a-input-number v-model="form.other_amount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
            <a-col :span="4">
              <a-form-model-item label="总计金额(元)" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number :value="totalAmount" :disabled="true" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
          </a-row>

          <a-row gutter="16">
            <a-col :span="4">
              <a-form-model-item label="结算账户" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-select v-model="sales_return_account_item.account" style="width: 100%">
                  <a-select-option v-for="Account in accountsItems" :key="Account.id" :value="Account.id">
                    {{ Account.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="4">
              <a-form-model-item label="实付金额(元)" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number v-model="sales_return_account_item.payment_amount" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
          </a-row>
          <a-row gutter="16">
            <a-col :span="4">
              <a-form-model-item label="本单欠款(元)" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number :value="amountOwed" :disabled="true" style="width: 100%;" />
              </a-form-model-item>
            </a-col>
          </a-row>
        </div>

        <!-- <div>
          <a-row gutter="16">
            <a-space>
              <a-button type="primary" @click="handelAddAcount">添加结算账户</a-button>
            </a-space>
          </a-row>
          <div style="margin-top: 16px;">
              <a-table rowKey="id" size="middle" :columns="columnsAccount" :data-source="accountsData"
                :pagination="false">
                <div slot="account" slot-scope="value, item, index">
                  <a-select v-if="!item.isTotal" v-model="item.account" style="width: 100%" @change="(value) => changeAccount(value, item, index)">
                    <a-select-option v-for="Account in accountsItems" :key="Account.id"
                      :value="Account.id">
                      {{ Account.name }}
                    </a-select-option>
                  </a-select>
                </div>
                <div slot="payment_amount" slot-scope="value, item, index">
                  <div v-if="item.isTotal">{{ value }}</div>
                  <a-input-number v-else style="width: 100%"
                    v-model="item.payment_amount"
                    :min="0"
                    :precision="2"></a-input-number>
                </div>
                <div slot="action" slot-scope="value, item, index">
                  <a-button-group v-if="!item.isTotal" size="small">
                    <a-button type="danger" @click="removeAccount(item)">移除</a-button>
                  </a-button-group>
                </div>
              </a-table>
          </div>
        </div> -->
      </a-spin>

      <div style="margin-top: 32px;">
        <a-popconfirm title="确定创建吗?" @confirm="create">
          <a-button type="primary" :loading="loading">创建</a-button>
        </a-popconfirm>
      </div>
    </a-card>
    <materials-select-modal v-model="materialsSelectModalVisible" :warehouse="form.warehouse" @select="onSelectMaterial"></materials-select-modal>
  </div>
</template>

<script>
  import moment from 'moment';
  import { getSaleReturnOrderNumber } from '@/api/data'
  import { saleReturnOrderCreate } from '@/api/sale';
  import { userOption, clientsOption, warehousesOption, inventoriesOption, accountsOption, saleOrdersOption } from '@/api/option'
  import NP from 'number-precision'

  export default {
    components: {
      MaterialsSelectModal: () => import('@/components/MaterialSelectModal/index'),
    },
    data() {
      return {
        description: '新增',
        saleOrdersItems: [],
        warehouseItems: [],
        handlerItems: [],
        clientsItems: [],
        accountsItems: [],
        materialsSelectModalVisible: false,
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
          client: [
            { required: true, message: '请选择客户', trigger: 'change' }
          ],
          handler: [
            { required: true, message: '请选择经手人', trigger: 'change' }
          ],
          handle_time: [
            { required: true, message: '请选择处理日期', trigger: 'change' },
          ],
          other_amount: [
            { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: '其他费用格式不正确', trigger: 'change' }
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
            title: '退货数量',
            dataIndex: 'return_quantity',
            key: 'return_quantity',
            width: 120,
            scopedSlots: { customRender: 'return_quantity' },
          },
          {
            title: '退货单价(元)',
            dataIndex: 'return_price',
            key: 'return_price',
            width: 120,
            scopedSlots: { customRender: 'return_price' },
          },
          {
            title: '金额',
            dataIndex: 'totalAmount',
            key: 'totalAmount',
            width: 200,
            customRender: (value, item) => {
              if (item.isTotal) return value;
              value = NP.times(item.return_quantity, item.return_price);
              return item.id ? NP.round(value, 2) : ''
            },
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
        columnsAccount: [
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
            title: '结算账户',
            dataIndex: 'account',
            key: 'account',
            width: 200,
            scopedSlots: { customRender: 'account' },
          },
          {
            title: '付款金额',
            dataIndex: 'payment_amount',
            key: 'payment_amount',
            width: 200,
            scopedSlots: { customRender: 'payment_amount' },
          },
          {
            title: '操作',
            dataIndex: 'action',
            key: 'action',
            width: 80,
            scopedSlots: { customRender: 'action' },
          },
        ],
        sales_return_account_items: [],
        sales_return_account_item: {},
      }
    },
    computed: {
      totalAmount() {
      let totalAmount = 0;
      for (let item of this.materialItems) {
        let amount = NP.times(item.return_quantity, item.return_price);
        totalAmount = NP.plus(totalAmount, amount);
      }

      totalAmount = NP.times(totalAmount, this.form.discount || 100, 0.01);
      totalAmount = NP.plus(totalAmount, this.form.other_amount || 0);
      return totalAmount;
    },
    amountOwed() {
      return NP.minus(this.totalAmount, this.sales_return_account_item.payment_amount || 0);
    },
      goodsData() {
        // 统计合计
        let totalQuantity = 0,
          totalAmount = 0;
        for (let item of this.materialItems) {
          totalQuantity = NP.plus(totalQuantity, item.return_quantity);
          let amount = NP.times(item.return_quantity, item.return_price);
          totalAmount = NP.plus(totalAmount, amount);
        }
        return [
          ...this.materialItems,
          {
            id: '-1',
            isTotal: true,
            name: '',
            return_quantity: totalQuantity,
            totalAmount: `${totalAmount} * ${this.form.discount}% = ${NP.times(
              totalAmount,
              this.form.discount || 0,
              0.01
            )}`,
          },
        ];
      },
      accountsData() {
        // 统计合计
        let totalAmount = 0;
        for (let item of this.sales_return_account_items) {
          totalAmount = NP.plus(totalAmount, item.payment_amount);
        }
        return [
          ...this.sales_return_account_items,
          {
            id: '-1',
            isTotal: true,
            payment_amount: totalAmount,
          },
        ];
      },
    },
    methods: {
      moment,
      initData() {
        this.resetForm();
        saleOrdersOption({ page_size: 999999, is_void: false }).then(data => {
          this.saleOrdersItems = data.results;
        });
        warehousesOption({ page_size: 999999, is_active: true }).then(data => {
          this.warehouseItems = data.results;
        });
        userOption({ page_size: 999999, is_active: true }).then(data => {
          this.handlerItems = data.results;
        });
        clientsOption({ page_size: 999999, is_active: true }).then(data => {
          this.clientsItems = data.results;
        });
        accountsOption({ page_size: 999999, is_active: true }).then(data => {
          this.accountsItems = data.results;
        });
      },
      changeRelatedOrder(value, option) {
        let selected = this.saleOrdersItems.filter(item => item.id == value)[0];
        this.form.client = selected.client;
        this.form.warehouse = selected.warehouse;
        this.form.handler = selected.handler;
        selected.sales_goods_items.map(item => {
          this.onSelectMaterial({...item, ...{ goods_spec: item.goods_spec || '', retail_price: item.sales_price }})
        })
      },
      handelAddAcount() {
        this.sales_return_account_items.push({
          id: this.sales_return_account_items.length + 1,
          account: '',
          payment_amount: 0
        });
      },
      removeAccount(item) {
        this.sales_return_account_items = this.$functions.removeItem(this.sales_return_account_items, item);
      },
      changeAccount(value, item, idx) {
        let count = this.sales_return_account_items.filter((_item) => {
          return _item.account == value;
        })
        if (count.length > 1) {
          this.$message.warn('已添加过改结算账户!');
          this.sales_return_account_items[idx].account = '';
        }
      },
      openMaterialModal() {
        if (!this.form.warehouse) {
          this.$message.warn('请先选择仓库！');
          return false;
        }
        this.materialsSelectModalVisible = true;
      },
      onSelectMaterial(item) {
        let index = this.materialItems.findIndex(_item => _item.goods == item.goods);
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
          return_quantity: 1,
          return_price: item.retail_price,
          totalAmount: 1
        });
      },
      removeMaterial(item) {
        this.materialItems = this.$functions.removeItem(this.materialItems, item);
      },
      create() {
        this.$refs.form.validate(async (valid) => {
          if (valid) {
            let ifHasEmptyGoods = false;
            let ifHasEmptyAccounts = false;
            
            // this.sales_return_account_items.map(item => {
            //   if (!item.account || item.payment_amount === '' || item.payment_amount === null) {
            //     ifHasEmptyAccounts = true;
            //   }
            // })
            // if (ifHasEmptyAccounts) {
            //   this.$message.warn('请将结算账户信息填写完整');
            //   return false
            // }

            if (this.materialItems.length == 0) {
              this.$message.warn('未添加产品');
              return false
            }
            this.materialItems.map(item => {
              if (item.return_price === null || !item.return_quantity) {
                ifHasEmptyGoods = true;
              }
            })
            if (ifHasEmptyGoods) {
              this.$message.warn('退货单价和销退货数量必填');
              return false
            }

            let sales_return_account_items = [];
          if (this.sales_return_account_item.account && this.sales_return_account_item.payment_amount > 0) {
            sales_return_account_items = [this.sales_return_account_items];
          }


            this.loading = true;
            let formData = {
              ...this.form,
              // sales_return_account_items: this.sales_return_account_items.map(item => {
              //   delete item.id
              //   return item
              // }),
              sales_return_account_items,
              sales_return_goods_items: this.materialItems.map(item => {
                if (this.form.sales_order) {
                  return {
                    sales_goods: item.id,
                    goods: item.goods,
                    return_quantity: item.return_quantity,
                    return_price: item.return_price,
                  }
                } else {
                  return {
                    goods: item.goods,
                    return_quantity: item.return_quantity,
                    return_price: item.return_price,
                  }
                }
              })
            };
            saleReturnOrderCreate(formData).then(data => {
              this.$message.success('创建成功');
              this.$router.push({ path: '/sale/sale_return_record' });
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      resetForm() {
        this.form = { other_amount: 0 };
      this.sales_return_account_item = { payment_amount: 0 };

        getSaleReturnOrderNumber().then(data => {
          this.form = { ...this.form, number: data.number, discount: 100 }
        })
        this.materialItems = [];
        this.handelAddAcount();
      },
    },
    mounted() {
      this.initData();
    }
  }
</script>
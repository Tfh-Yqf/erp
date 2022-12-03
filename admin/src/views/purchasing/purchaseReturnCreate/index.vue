<template>
  <div>
    <a-card title="采购退货单">
      <a-spin :spinning="loading">
        <a-form-model ref="form" :model="form" :rules="rules" :label-col="{ span: 8 }" :wrapper-col="{ span: 16 }">
          <a-row>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="number" label="退货单编号">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="purchase_order" label="采购单据">
                <a-select v-model="form.purchase_order" @change="changeRelatedOrder" style="width: 100%">
                  <a-select-option v-for="item in purchaseOrdersItems" :key="item.id" :value="item.id">
                    {{ item.number }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="6" style="width: 320px;">
              <a-form-model-item prop="supplier" label="供应商">
                <a-select v-model="form.supplier" style="width: 100%">
                  <a-select-option v-for="item in suppliersItems" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </a-select-option>
                </a-select>
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
            <!-- <a-col :span="6" style="width: 320px;">
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
            <a-table rowKey="id" size="middle" :columns="columns" :data-source="goodsData" :pagination="false">
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
                <a-select v-model="purchase_return_account_item.account" style="width: 100%">
                  <a-select-option v-for="Account in accountsItems" :key="Account.id" :value="Account.id">
                    {{ Account.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="4">
              <a-form-model-item label="实收金额(元)" :label-col="{ span: 24 }" :wrapper-col="{ span: 24 }">
                <a-input-number v-model="purchase_return_account_item.collection_amount" style="width: 100%;" />
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
                <div slot="collection_amount" slot-scope="value, item, index">
                  <div v-if="item.isTotal">{{ value }}</div>
                  <a-input-number v-if="!item.isTotal" style="width: 100%"
                    v-model="item.collection_amount"
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
    <materials-select-modal
      v-model="materialsSelectModalVisible"
      :warehouse="form.warehouse"
      @select="onSelectMaterial"
    ></materials-select-modal>
  </div>
</template>

<script>
import moment from "moment";
import { getPurchaseReturnOrderNumber } from "@/api/data";
import { purchaseReturnOrderCreate } from "@/api/purchasing";
import {
  suppliersOption,
  userOption,
  warehousesOption,
  inventoriesOption,
  accountsOption,
  purchaseOrdersOption,
} from "@/api/option";
import NP from 'number-precision'

export default {
  components: {
    MaterialsSelectModal: () => import("@/components/MaterialSelectModal/index"),
  },
  data() {
    return {
      description: "新增",
      purchaseOrdersItems: [],
      warehouseItems: [],
      handlerItems: [],
      suppliersItems: [],
      accountsItems: [],
      materialsSelectModalVisible: false,
      loading: false,
      model: {},
      form: {},
      rules: {
        number: [{ required: true, message: "请输入退货单编号", trigger: "change" }],
        warehouse: [{ required: true, message: "请选择仓库", trigger: "change" }],
        supplier: [{ required: true, message: "请选择供应商", trigger: "change" }],
        handler: [{ required: true, message: "请选择经手人", trigger: "change" }],
        handle_time: [{ required: true, message: "请选择处理日期", trigger: "change" }],
        other_amount: [
          { pattern: new RegExp(/^\d{0,14}(?:\.\d{0,2})?$/), message: "其他费用格式不正确", trigger: "change" },
        ],
      },
      columns: [
        {
          title: "序号",
          dataIndex: "index",
          key: "index",
          width: 45,
          customRender: (value, item, index) => {
            return item.isTotal ? "合计" : index + 1;
          },
        },
        {
          title: "名称",
          dataIndex: "name",
          key: "name",
          width: 150,
        },
        {
          title: "编号",
          dataIndex: "number",
          key: "number",
          width: 150,
        },
        {
          title: "规格",
          dataIndex: "spec",
          key: "spec",
          width: 150,
        },
        {
          title: "单位",
          dataIndex: "unit",
          key: "unit",
          width: 80,
        },
        {
          title: "退货数量",
          dataIndex: "return_quantity",
          key: "return_quantity",
          width: 120,
          scopedSlots: { customRender: "return_quantity" },
        },
        {
          title: "退货单价(元)",
          dataIndex: "return_price",
          key: "return_price",
          width: 120,
          scopedSlots: { customRender: "return_price" },
        },
        {
          title: "金额",
          dataIndex: "totalAmount",
          key: "totalAmount",
          width: 200,
          customRender: (value, item) => {
            if (item.isTotal) return value;
            value = NP.times(item.return_quantity, item.return_price);
            return item.id ? NP.round(value, 2) : "";
          },
        },
        {
          title: "操作",
          dataIndex: "action",
          key: "action",
          width: 80,
          scopedSlots: { customRender: "action" },
        },
      ],
      materialItems: [],
      columnsAccount: [
        {
          title: "序号",
          dataIndex: "index",
          key: "index",
          width: 45,
          customRender: (value, item, index) => {
            return item.isTotal ? "合计" : index + 1;
          },
        },
        {
          title: "结算账户",
          dataIndex: "account",
          key: "account",
          width: 200,
          scopedSlots: { customRender: "account" },
        },
        {
          title: "收款金额",
          dataIndex: "collection_amount",
          key: "collection_amount",
          width: 200,
          scopedSlots: { customRender: "collection_amount" },
        },
        {
          title: "操作",
          dataIndex: "action",
          key: "action",
          width: 80,
          scopedSlots: { customRender: "action" },
        },
      ],
      purchase_return_account_items: [],
      purchase_return_account_item: {},
    };
  },
  computed: {
    totalAmount() {
      let totalAmount = 0;
      for (let item of this.materialItems) {
        let amount = NP.times(item.return_quantity, item.return_price);
        totalAmount = NP.plus(totalAmount, amount);
      }

      totalAmount = NP.plus(totalAmount, this.form.other_amount || 0);
      return totalAmount;
    },
    amountOwed() {
      return NP.minus(this.totalAmount, this.purchase_return_account_item.collection_amount || 0);
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
          id: "-1",
          isTotal: true,
          name: "",
          return_quantity: totalQuantity,
          totalAmount: totalAmount,
        },
      ];
    },
    accountsData() {
      // 统计合计
      let totalAmount = 0;
      for (let item of this.purchase_return_account_items) {
        totalAmount = NP.plus(totalAmount, item.collection_amount);
      }
      return [
        ...this.purchase_return_account_items,
        {
          id: "-1",
          isTotal: true,
          collection_amount: totalAmount,
        },
      ];
    },
  },
  methods: {
    moment,
    initData() {
      this.resetForm();
      purchaseOrdersOption({ page_size: 999999, is_void: false }).then((data) => {
        this.purchaseOrdersItems = data.results;
      });
      warehousesOption({ page_size: 999999, is_active: true }).then((data) => {
        this.warehouseItems = data.results;
      });
      userOption({ page_size: 999999, is_active: true }).then((data) => {
        this.handlerItems = data.results;
      });
      suppliersOption({ page_size: 999999, is_active: true }).then((data) => {
        this.suppliersItems = data.results;
      });
      accountsOption({ page_size: 999999, is_active: true }).then((data) => {
        this.accountsItems = data.results;
      });
    },
    changeRelatedOrder(value, option) {
      let selected = this.purchaseOrdersItems.filter(item => item.id == value)[0];
      this.form.supplier = selected.supplier;
      this.form.warehouse = selected.warehouse;
      this.form.handler = selected.handler;
      selected.purchase_goods_items.map(item => {
        this.onSelectMaterial({...item, ...{ goods_spec: item.goods_spec || '', total_quantity: item.total_amount }})
      })
    },
    handelAddAcount() {
      this.purchase_return_account_items.push({
        id: this.purchase_return_account_items.length + 1,
        account: "",
        collection_amount: 0,
      });
    },
    removeAccount(item) {
      this.purchase_return_account_items = this.$functions.removeItem(this.purchase_return_account_items, item);
    },
    changeAccount(value, item, idx) {
      let count = this.purchase_return_account_items.filter((_item) => {
        return _item.account == value;
      });
      if (count.length > 1) {
        this.$message.warn("已添加过改结算账户!");
        this.purchase_return_account_items[idx].account = "";
      }
    },
    changeWarehouse() {
      this.materialItems = [];
    },
    openMaterialModal() {
      if (!this.form.warehouse) {
        this.$message.warn("请先选择仓库！");
        return false;
      }
      this.materialsSelectModalVisible = true;
    },
    onSelectMaterial(item) {
      let index = this.materialItems.findIndex((_item) => _item.goods == item.goods);
      if (index != -1) {
        this.$message.warn("产品已存在");
        return;
      }
      this.materialItems = this.$functions.insertItem(this.materialItems, {
        id: item.id,
        goods: item.goods,
        number: item.goods_number,
        name: item.goods_name,
        spec: item.goods_spec,
        unit: item.unit_name,
        return_quantity: 1,
        return_price: item.purchase_price,
        total_quantity: item.total_quantity,
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

          // this.purchase_return_account_items.map((item) => {
          //   console.log(item.collection_amount);
          //   if (!item.account || item.collection_amount === "" || item.collection_amount === null) {
          //     ifHasEmptyAccounts = true;
          //   }
          // });
          // if (ifHasEmptyAccounts) {
          //   this.$message.warn('请将结算账户信息填写完整');
          //   return false
          // }

          if (this.materialItems.length == 0) {
            this.$message.warn("未添加产品");
            return false;
          }
          this.materialItems.map((item) => {
            if (item.return_price === null || !item.return_quantity) {
              ifHasEmptyGoods = true;
            }
          });
          if (ifHasEmptyGoods) {
            this.$message.warn("退货单价退货数量必填");
            return false;
          }

          let purchase_return_account_items = [];
          if (this.purchase_return_account_item.account && this.purchase_return_account_item.collection_amount > 0) {
            purchase_return_account_items = [this.purchase_return_account_item];
          }

          this.loading = true;
          let formData = {
            ...this.form,
            // purchase_return_account_items: this.purchase_return_account_items.map(item => {
            //   delete item.id
            //   return item
            // }),
            purchase_return_account_items,
            purchase_return_goods_items: this.materialItems.map((item) => {
              if (this.form.purchase_order) {
                return {
                  purchase_goods: item.id,
                  goods: item.goods,
                  return_quantity: item.return_quantity,
                  return_price: item.return_price,
                };
              } else {
                return {
                  goods: item.goods,
                  return_quantity: item.return_quantity,
                  return_price: item.return_price,
                };
              }
              
            }),
          };
          console.log(formData);
          purchaseReturnOrderCreate(formData)
            .then((data) => {
              this.$message.success("创建成功");
              this.$router.push({ path: "/purchasing/return_record" });
            })
            .finally(() => {
              this.loading = false;
            });
        }
      });
    },
    resetForm() {
      this.form = { other_amount: 0 };
      this.purchase_return_account_item = { collection_amount: 0 };
      getPurchaseReturnOrderNumber().then((data) => {
        this.form = { ...this.form, number: data.number };
      });
      this.materialItems = [];
      this.handelAddAcount();
    },
  },
  mounted() {
    this.initData();
  },
};
</script>

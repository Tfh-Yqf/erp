<template>
  <div>
    <a-modal v-model="visible" width="750px" :confirmLoading="loading" :maskClosable="false" @cancel="cancel" @ok="confirm">
      <div slot="title">{{form.id ? '编辑产品信息' : '新增产品信息' }}</div>
      <div>
        <a-form-model
          ref="form"
          :model="form"
          :rules="rules"
          :label-col="{ span: 4, md: 8 }"
          :wrapper-col="{ span: 20, md: 16 }">
          <a-row gutter="12">
            <a-divider orientation="left" id="basic-information">
              基本信息
            </a-divider>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="barcode" label="条形码">
                <a-input v-model="form.barcode" />
                <!-- <a-input-search v-model="form.barcode">
                  <a-button slot="enterButton" type="primary" @click.native="getCode">生成条形码</a-button>
                </a-input-search> -->
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="number" label="产品编号">
                <a-input v-model="form.number" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="name" label="产品名称">
                <a-input v-model="form.name" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="category" label="分类">
                <a-select v-model.number="form.category" style="width: 100%" :allowClear="true">
                  <a-select-option
                    v-for="item of classificationItems"
                    :key="item.id"
                    :value="item.id">{{ item.name }}
                  </a-select-option>
                </a-select>
                <!-- <a-button
                  type="primary"
                  style="width: 20%; margin-left: 5%"
                  @click="
                    resetForm();
                    categoryVisible = true;">
                  <a-icon type="plus" />
                </a-button> -->
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="unit" label="单位">
                <a-select v-model.number="form.unit" :allowClear="true">
                  <a-select-option
                    v-for="item of unitItems"
                    :key="item.id"
                    :value="item.id">{{ item.name }}
                  </a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="spec" label="规格">
                <a-input v-model="form.spec" />
              </a-form-model-item>
            </a-col>
            <!-- <a-col :span="24" :md="12">
              <a-form-model-item prop="enable_shelf_life" label="启用保质期">
                <a-switch
                  checked-children="启用"
                  un-checked-children="禁用"
                  v-model="form.enable_shelf_life"/>
              </a-form-model-item>
            </a-col> -->
            <a-col :span="24" :md="12">
              <a-form-model-item prop="shelf_life_days" label="保质期天数">
                <a-input v-model="form.shelf_life_days" suffix="天" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item
                prop="shelf_life_warning_days"
                label="保质期预警天数">
                <a-input v-model="form.shelf_life_warning_days" suffix="天" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="enable_batch_control" label="启用批次控制">
                <a-switch
                  checked-children="启用"
                  un-checked-children="禁用"
                  v-model="form.enable_batch_control"
                />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="is_active" label="状态">
                <a-select v-model="form.is_active" style="width: 100%;">
                  <a-select-option :value="true">激活</a-select-option>
                  <a-select-option :value="false">冻结</a-select-option>
                </a-select>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="remark" label="备注">
                <a-input v-model="form.remark" allowClear />
              </a-form-model-item>
            </a-col>
          </a-row>
          <a-row gutter="12">
            <a-divider orientation="left" id="price-management">
              价格管理
            </a-divider>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="purchase_price" label="采购价(元)">
                <a-input-number v-model="form.purchase_price" style="width: 100%"/>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="retail_price" label="零售价(元)">
                <a-input-number v-model="form.retail_price" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="level_price1" label="等级价一(元)">
                <a-input-number v-model="form.level_price1" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="level_price2" label="等级价二(元)">
                <a-input-number v-model="form.level_price2" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="level_price3" label="等级价三(元)">
                <a-input-number v-model="form.level_price3" style="width: 100%" />
              </a-form-model-item>
            </a-col>
          </a-row>
          <a-row gutter="12">
            <a-divider orientation="left" id="graphic-information">
              图文信息
            </a-divider>
            <a-col :span="24" :md="24">
              <a-upload
                action="/api/goods_images/"
                list-type="picture-card"
                :headers="{ 'X-CSRFToken': Cookies.get('csrftoken') }"
                :file-list="form.image_items"
                @preview="handlePreview"
                @change="handleChange"
                :before-upload="beforeUpload"
                name="file">
                <div>
                  <a-icon type="plus" />
                  <div class="ant-upload-text"></div>
                </div>
              </a-upload>
              <a-modal
                :visible="previewVisible"
                :footer="null"
                @cancel="handleCancel"
              >
                <img alt="example" style="width: 100%" :src="previewImage" />
              </a-modal>
            </a-col>
            <a-col :span="24" :md="24">
              <a-textarea
                placeholder="产品详细介绍"
                :rows="4"
                v-model="form.description"
              />
            </a-col>
          </a-row>
          <a-row gutter="12">
            <a-divider orientation="left" id="beginning-inventory">
              期初库存
            </a-divider>
            <a-col :span="24" :md="24">
              <a-table
                rowkey="id"
                :columns="columns"
                :data-source="warehouseItems"
                :loading="loading"
                :pagination="false"
                style="width: 100%" >
                <div slot="initial_quantity" slot-scope="value, item">
                  <div v-if="!!form.enable_batch_control">
                    <a-input :value="item.initial_quantity" disabled style="width:75%;" />
                    <a-button @click="chooseBatch(item)">批</a-button>
                  </div>
                  <a-input-number v-else
                    :value="item.initial_quantity"
                    min="1"
                    @change="(value) => changeQuantity(value, item)" />
                </div>
              </a-table>
            </a-col>
          </a-row>
          <a-row gutter="12">
            <a-divider orientation="left" id="inventory-warning">
              库存预警
            </a-divider>
            <a-col :span="24" :md="12">
              <a-form-model-item prop="enable_inventory_warning" label="启用库存警告">
                <a-switch
                  checked-children="启用"
                  un-checked-children="禁用"
                  v-model="form.enable_inventory_warning"/>
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12" v-if="!!form.enable_inventory_warning">
              <a-form-model-item prop="inventory_upper" label="库存上限">
                <a-input-number v-model="form.inventory_upper" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12" v-if="!!form.enable_inventory_warning">
              <a-form-model-item prop="inventory_lower" label="库存下限">
                <a-input-number v-model="form.inventory_lower" style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <!-- <a-col :span="24" :md="12">
              <a-form-model-item
                prop="inventory_warning_upper_limit"
                label="库存预警上限">
                <a-input-number
                  v-model="form.inventory_warning_upper_limit"
                  style="width: 100%" />
              </a-form-model-item>
            </a-col>
            <a-col :span="24" :md="12">
              <a-form-model-item
                prop="inventory_warning_lower_limit"
                label="库存预警下限">
                <a-input-number
                  v-model="form.inventory_warning_lower_limit"
                  style="width: 100%"/>
              </a-form-model-item>
            </a-col> -->
          </a-row>
        </a-form-model>
      </div>
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
          :data-source="batchItems"
          :pagination="false"
          style="width: 100%" >
          <div slot="initial_quantity" slot-scope="value, item">
            <a-input-number
              :value="item.initial_quantity"
              min="1"
              @change="(value) => changeQuantityBatch(value, item, 'initial_quantity')" />
          </div>
          <div slot="number" slot-scope="value, item">
            <a-input
              :value="item.number"
              @change="(e) => changeQuantityBatch(e, item, 'number')" />
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

    </a-modal>
  </div>
</template>

<script>
  import Cookies from 'js-cookie'
  import { goodsInformationCreate, goodsInformationUpdate } from '@/api/goods'
  function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });
  }
  export default {
    name: 'FormModal',
    props: ['visible', 'form', 'warehouseItems', 'classificationItems', 'unitItems'],
    model: { prop: 'visible', event: 'cancel' },
    data() {
      return {
        Cookies,
        batchTitle: '管理批次',
        batchVisible: false,
        loading: false,
        columns: [
          {
            title: "仓库",
            dataIndex: "name",
            key: "name",
          },
          {
            title: "初始库存",
            dataIndex: "initial_quantity",
            key: "initial_quantity",
            scopedSlots: { customRender: "initial_quantity" },
          },
        ],
        isKeepAdd: false,
        categoryForm: {},
        categoryVisible: false,
        rules: {
          name: [
            { required: true, message: "请输入产品名称", trigger: "change" },
          ],
          number: [
            { required: true, message: "请输入产品编号", trigger: "change" },
          ],
        },
        previewVisible: false,
        previewImage: "",
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
            dataIndex: "number",
            key: "number",
            scopedSlots: { customRender: "number" },
          },
          {
            title: "初始库存",
            dataIndex: "initial_quantity",
            key: "initial_quantity",
            scopedSlots: { customRender: "initial_quantity" },
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
        curWarehouse: {},
        batchItems: []
      };
    },
    methods: {
      chooseBatch(item) {
        this.batchTitle = '管理批次-' + item.name;
        this.curWarehouse = item;
        if (item.batch_items) {
          this.batchItems = item.batch_items;
        } else {
          this.batchItems = [
            {
              key: 'uni1',
              number: '',
              initial_quantity: 1,
              production_date: null,
            }
          ];
        }
        this.batchVisible = true;
      },
      confirmChoosed() {
        let ifHasEmpty = false;
        let sumAmount = 0;
        this.batchItems.map(item => {
          sumAmount+=item.initial_quantity
          if (!item.number || !item.initial_quantity || !item.production_date) {
            ifHasEmpty = true;
          }
        })
        if (ifHasEmpty) {
            this.$message.warn('请将批次信息填写完整!');
            return
          }
        let tmp = {...this.curWarehouse, ...{ batch_items: this.batchItems, initial_quantity: sumAmount }}
        this.warehouseItems = this.$functions.replaceItem(this.warehouseItems, tmp);
        this.batchVisible = false;
      },
      addLine() {
        const { batchItems } = this;
        const newData = {
          key: 'uni' + batchItems.length + 1,
          number: '',
          initial_quantity: 1,
          production_date: null,
        };
        this.batchItems = [...batchItems, newData];
      },
      removeLine(item) {
        this.batchItems = this.$functions.removeItemBatch(this.batchItems, item);
      },
      changeQuantity(value, item) {
        item['initial_quantity'] = value || 0;
        this.warehouseItems = this.$functions.replaceItem(this.warehouseItems, item);
      },
      changeQuantityBatch(e, item, pro) {
        if (pro === 'number') {
          item[pro] = e.target.value;
        } else {
          item[pro] = e;
        }
        this.batchItems[item.key - 1] = item;
      },
      async handlePreview(file) {
        if (!file.url && !file.preview) {
          file.preview = await getBase64(file.originFileObj);
        }
        this.previewImage = file.url || file.preview;
        this.previewVisible = true;
      },
      handleChange({ fileList }) {
        this.$set(this.form,'image_items',fileList);
      },
      beforeUpload() {},
      handleCancel() {
        this.previewVisible = false;
      },
      confirm() {
        let image_items = this.form.image_items.map(item => { return item.response.id })
        let inventory_items = this.warehouseItems.map(item => {
          return {
            warehouse: item.id,
            initial_quantity: item.initial_quantity,
            batch_items: this.form.enable_batch_control ? item.batch_items : []
          }
        })
        let formatData = {
          ...this.form,
          ...{
            goods_images: image_items,
            inventory_items
          }
        }
        console.log(formatData)
        this.$refs.form.validate(valid => {
          if (valid) {
            this.loading = true;
            let func = this.form.id ? goodsInformationUpdate : goodsInformationCreate;
            func(formatData).then(data => {
              this.$message.success(this.form.id ? '修改成功' : '新增成功');
              this.$emit(this.form.id ? 'update' : 'create', data);
              this.cancel();
            }).finally(() => {
              this.loading = false;
            });
          }
        });
      },
      cancel() {
        this.$emit('cancel', false);
        this.$refs.form.resetFields();
      },
    },
    watch: {
      // 'form.image_items': {
      //   handler(newVal) {
      //     if (Array.isArray(newVal)) {
      //       var images = newVal.map((file)=>{
      //         if (file.status) {
      //           if (file.status == 'done') {
      //             if (file.response && file.response.id) {
      //               return file.response.id;
      //             }
      //             if (file.uid) {
      //             return file.uid;
      //           }
      //           } 
      //         } 
      //       });
      //       this.$set(this.form,'images',images);
      //     }
      //   },
      //   deep: true
      // },
    }
  }
</script>

<style scoped>
</style>
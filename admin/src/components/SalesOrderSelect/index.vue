<template>
  <div>
    <a-select
      v-model="value"
      :placeholder="placeholder"
      allowClear
      show-search
      :disabled="disabled"
      :filter-option="false"
      :not-found-content="loading ? undefined : '暂无数据'"
      style="width: 100%;"
      @search="search"
      @change="change"
      @focus="focus"
      @popupScroll="scroll"
    >
      <div slot="notFoundContent" style="text-align: center;">
        <a-spin size="small" :spinning="loading" />
      </div>

      <a-select-option v-for="item in options" :key="item.id" :value="item.id">
        {{ item.number }}
      </a-select-option>

      <a-select-option v-if="!isloadedAll" key="loading" value="loading" disabled>
        <div style="text-align: center; height: 24px;">
          <a-spin size="small" :spinning="loading" />
        </div>
      </a-select-option>
    </a-select>
  </div>
</template>

<script>
import { saleOrdersOption } from "@/api/option";

export default {
  props: ["value", "placeholder", "disabled", "defaultItem"],
  model: { prop: "value", event: "change" },
  data() {
    return {
      items: [],
      searchForm: { search: "", page: 1, is_active: true, page_size: 16 },
      totalRows: 0,
      loading: false,
      timeout: null,
    };
  },
  computed: {
    options() {
      let items = [...this.items];
      if (this.defaultItem && !this.loading && (!this.searchForm.search || this.searchForm.search == "")) {
        if (this.defaultItem.sales_order && this.defaultItem.sales_order_number) {
          if (this.items.findIndex((item) => item.id == this.value) == -1) {
            items.splice(0, 0, { id: this.defaultItem.sales_order, number: this.defaultItem.sales_order_number });
          }
        }
      }
      return items;
    },
    isloadedAll() {
      return this.searchForm.page * this.searchForm.page_size >= this.totalRows;
    },
  },
  methods: {
    list() {
      if (this.searchForm.page === 1) {
        this.items = [];
      }

      this.loading = true;
      saleOrdersOption(this.searchForm)
        .then((data) => {
          this.totalRows = data.count;
          this.items.push(...data.results);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    change(value) {
      this.$emit("change", value);
      let index = this.items.findIndex((item) => item.id == value);
      if (index != -1) {
        this.$emit("select", this.items[index]);
      }
    },
    focus() {
      this.searchForm.page = 1;
      this.list();
    },
    scroll({ target }) {
      if (!this.loading && target.scrollTop + target.offsetHeight === target.scrollHeight) {
        if (!this.isloadedAll) {
          this.searchForm.page += 1;
          this.list();
        }
      }
    },
    search(value) {
      this.searchForm.page = 1;
      this.searchForm.search = value;
      if (this.timeout) {
        clearTimeout(this.timeout);
        this.timeout = null;
      }
      this.timeout = setTimeout(this.list, 300);
    },
  },
};
</script>

<style scoped></style>

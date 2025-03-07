<template>
  <div>
    <GenericListPage
      ref="GenericListPage"
      :create-drawer="createDrawer"
      :detail-drawer="detailDrawer"
      :header-actions="headerActions"
      :table-config="tableConfig"
    />
    <Dialog
      :title="$tc('Import')"
      :visible.sync="dialogImport"
      top="20vh"
      width="600px"
      @cancel="dialogImport = false"
      @confirm="importData"
    >
      <div style="padding-bottom: 10px">
        商品的 Excel 文件
      </div>
      <input type="file" @change="fileChange">
    </Dialog>
  </div>
</template>

<script>
import { GenericListPage } from '@/layout/components'
import { Dialog } from '@/components'
import request from '@/utils/request'
import DetailFormatter from '@/components/Table/TableFormatters/DetailFormatter.vue'

export default {
  components: {
    Dialog,
    GenericListPage
  },
  data() {
    const vm = this
    const hasDelete = () => {
      return vm.$hasPerm('products.delete_product')
    }
    return {
      dialogImport: false,
      importFile: {},
      createDrawer: () => import('./ProductCreateUpdate.vue'),
      detailDrawer: () => import('@/views/products/Product/ProductDetail/index.vue'),
      tableConfig: {
        url: '/api/v1/products/products/',
        permissions: {
          resource: 'product'
        },
        columnsExclude: [],
        columns: [
          'name', 'spu', 'skc', 'sku', 'avatar_url',
          'type', 'price', 'cost', 'number', 'actions'
        ],
        columnsShow: {
          min: ['name', 'sku', 'price', 'actions'],
          default: [
            'name', 'sku', 'avatar_url', 'type', 'price', 'cost', 'number', 'actions'
          ]
        },
        columnsMeta: {
          name: {
            formatter: DetailFormatter,
            formatterArgs: {
              getTitle: ({ row }) => row.name.slice(0, 20),
              drawer: true
            }
          },
          avatar_url: {
            formatter: DetailFormatter,
            formatterArgs: {
              avatar: true,
              getIcon({ col, row, cellValue }) {
                return row.avatar_url
              }
            }
          }
        }
      },
      headerActions: {
        hasLabelSearch: true,
        hasBulkDelete: hasDelete,
        canCreate: this.$hasPerm('products.add_product'),
        extraActions: [
          {
            name: this.$t('Import'),
            title: this.$t('Import'),
            can: () => vm.$hasPerm('products.change_product'),
            callback: () => {
              this.dialogImport = true
            }
          }
        ],
        hasBulkUpdate: false,
        extraMoreActions: [
        ]
      },
      InviteDialogSetting: {
        InviteDialogVisible: false
      }
    }
  },
  computed: {
  },
  mounted() {
  },
  methods: {
    importData() {
      if (this.importFile['file'] === undefined) {
        return
      }
      const formData = new FormData()
      formData.append('file', this.importFile['file'])
      request({
        url: '/api/v1/products/products/sync/',
        method: 'patch',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: formData
      }).then(res => {
        this.$message.success(res.msg)
        this.dialogImport = false
      }).catch(err => {
        this.$message.error(`Import failed ${err}`)
      })
    },
    fileChange(e) {
      this.importFile['file'] = e.target.files[0]
    },
    reloadTable() {
      this.$refs.GenericListPage.reloadTable()
    }
  }
}
</script>

<style lang="less" scoped>
.asset-select-dialog ::v-deep .transition-box:first-child {
  background-color: #f3f3f3;
}
</style>

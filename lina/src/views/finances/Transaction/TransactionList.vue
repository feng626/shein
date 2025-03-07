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
        {{ this.$t('LicenseFile') }}
      </div>
      <input type="file" @change="fileChange">
    </Dialog>
  </div>
</template>

<script>
import { GenericListPage } from '@/layout/components'
import { Dialog } from '@/components'
import request from '@/utils/request'

export default {
  components: {
    Dialog,
    GenericListPage
  },
  data() {
    const vm = this
    const hasDelete = () => {
      return vm.$hasPerm('finances.delete_transaction')
    }
    return {
      dialogImport: false,
      importFile: {},
      createDrawer: () => import('./TransactionCreateUpdate.vue'),
      detailDrawer: () => import('@/views/finances/Transaction/TransactionDetail/index.vue'),
      tableConfig: {
        url: '/api/v1/finances/transactions/',
        permissions: {
          resource: 'transaction'
        },
        columnsExclude: [],
        columns: [
          'name', 'amount', 'state', 'price', 'product', 'datetime', 'actions'
        ],
        columnsShow: {
          min: ['name', 'price', 'amount', 'actions'],
          default: [
            'name', 'amount', 'state', 'price', 'product', 'datetime', 'actions'
          ]
        },
        columnsMeta: {
        }
      },
      headerActions: {
        hasLabelSearch: true,
        hasDatePicker: true,
        hasBulkDelete: hasDelete,
        canCreate: this.$hasPerm('finances.add_transaction'),
        extraActions: [
          {
            name: this.$t('Import'),
            title: this.$t('Import'),
            can: () => vm.$hasPerm('finances.change_transaction'),
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
        url: '/api/v1/finances/transactions/sync/',
        method: 'patch',
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: formData
      }).then(res => {
        if (res.not_exists.length > 0) {
          this.$message.warning(`The following products do not exist: ${res.not_exists.join(', ')}`)
        } else {
          this.$message.success(res.msg)
        }
        this.dialogImport = false
        this.reloadTable()
      }).catch(err => {
        this.$message.error(`Import failed ${err}`)
      })
    },
    fileChange(e) {
      this.importFile['file'] = e.target.files[0]
    },
    reloadTable() {
      this.$refs.GenericListPage.$refs.ListTable.reloadTable()
    }
  }
}
</script>

<style lang="less" scoped>
.asset-select-dialog ::v-deep .transition-box:first-child {
  background-color: #f3f3f3;
}
</style>

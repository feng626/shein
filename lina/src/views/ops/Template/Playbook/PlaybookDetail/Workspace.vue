<template>
  <div>
    <NewNodeDialog v-if="createDialogVisible" :visible.sync="createDialogVisible" @confirm="doCreate" />
    <TreeTable ref="TreeTable" :tree-setting="treeSetting">
      <template v-if="!disableEdit" slot="rMenu">
        <li id="m_create_file" class="rmenu" tabindex="-1" @click="onCreate('file')">
          {{ $tc('NewFile') }}
        </li>
        <li id="m_create_directory" class="rmenu" tabindex="-1" @click="onCreate('directory')">
          {{ $tc('NewDirectory') }}
        </li>
        <li id="m_rename" class="rmenu" tabindex="-1" @click="onRename">
          {{ $tc('Rename') }}
        </li>
        <li id="m_delete" class="rmenu" tabindex="-1" @click="onDelete">
          {{ $tc('Delete') }}
        </li>
      </template>
      <template slot="table">
        <div class="transition-box" style="width: calc(100% - 17px);">
          <el-tabs v-model="activeEditorId" :closable="true" class="workspace-tab" @tab-remove="onCloseEditor">
            <el-tab-pane
              v-for="(editor,key) in openedEditor"
              :key="key"
              :label="tabLabel(editor)"
              :name="key"
            >
              <CodeEditor
                :options="cmOptions"
                :toolbar="toolbar"
                :value.sync="editor.value"
                style="margin-bottom: 20px"
              />
            </el-tab-pane>
          </el-tabs>
          <div style="display: flex;margin-top:10px;justify-content: space-between" />
          <el-form ref="form" label-position="left" label-width="30px">
            <div class="form-content">
              <el-form-item label="" prop="variable">
                <Variable :value.sync="variables" :disable-edit.sync="disableEdit" @input="setVariable" />
              </el-form-item>
            </div>
          </el-form>
        </div>
      </template>
    </TreeTable>
  </div>
</template>

<script>
import { TreeTable } from '@/components'
import CodeEditor from '@/components/Form/FormFields/CodeEditor'
import item from '@/layout/components/NavLeft/Item'
import NewNodeDialog from '@/views/ops/Template/Playbook/PlaybookDetail/Editor/NewNodeDialog.vue'
import { renameFile } from '@/api/ops'
import Variable from '@/views/ops/Template/components/Variable'

export default {
  name: 'CommandExecution',
  components: {
    NewNodeDialog,
    TreeTable,
    CodeEditor,
    Variable
  },
  props: {
    object: {
      type: Object,
      default: () => {
      }
    }
  },
  data() {
    const disableEdit = this.object.creator !== this.$store.state.users.profile.id
    return {
      disableEdit: disableEdit,
      newNode: {},
      createDialogVisible: false,
      createType: 'directory',
      parentId: '',
      closing: false,
      DataZTree: 0,
      cmOptions: {
        mode: 'yaml',
        readOnly: disableEdit
      },
      toolbar: {
        left: {
          save: {
            type: 'button',
            align: 'left',
            icon: 'fa fa-save',
            tip: this.$tc('Save'),
            el: {
              type: 'primary'
            },
            isVisible: disableEdit,
            callback: () => {
              this.onSave()
            }
          },
          reset: {
            type: 'button',
            align: 'left',
            icon: 'fa fa-undo',
            tip: this.$tc('Reset'),
            el: {
              type: 'primary'
            },
            isVisible: disableEdit,
            callback: () => {
              this.onReset()
            }
          }
        }
      },
      treeSetting: {
        async: false,
        treeUrl: `/api/v1/ops/playbook/${this.object.id}/file/`,
        showRefresh: true,
        showMenu: true,
        showDelete: false,
        showCreate: false,
        showUpdate: false,
        showSearch: false,
        callback: {
          onSelected: function(event, treeNode) {
            if (!treeNode.isParent) {
              this.onOpenEditor(treeNode)
            }
          }.bind(this),
          refresh: function(event, treeNode) {
          },
          onRename: function(event, treeId, treeNode, isCancel) {
            if (isCancel) {
              return
            }
            renameFile(this.object.id, {
              key: treeNode.id,
              new_name: treeNode.name,
              is_directory: treeNode.isParent
            }).then()
              .finally(() => {
                this.refreshTree()
              })
          }.bind(this)
        },
        check: {
          enable: false
        },
        view: {
          dblClickExpand: false,
          showLine: true
        }
      },
      iShowTree: true,
      activeEditorId: '',
      openedEditor: {},
      variables: []
    }
  },
  computed: {
    item() {
      return item
    },
    zTree() {
      return this.$refs.TreeTable.$refs.AutoDataZTree.$refs.dataztree.zTree
    },
    dataztree() {
      return this.$refs.TreeTable.$refs.AutoDataZTree
    },
    activeEditor() {
      return this.openedEditor[this.activeEditorId]
    },
    refreshTree() {
      return this.$refs.TreeTable.$refs.AutoDataZTree.$refs.dataztree.refresh
    }
  },
  mounted() {
    this.variables = this.object?.variable
    this.onOpenEditor({ id: 'main.yml', name: 'main.yml' })
  },
  methods: {
    refreshEditor(id, name) {
      this.openedEditor[id].name = name
    },
    onReset() {
      const editor = this.activeEditor
      editor.value = editor.originValue
    },
    onSave() {
      const editor = this.activeEditor
      this.$axios.patch(`/api/v1/ops/playbook/${this.object.id}/file/`,
        { key: this.activeEditorId, content: editor.value }).then(data => {
        editor.originValue = editor.value
        if (this.closing) {
          this.remoteTab(editor.key)
        }
        this.$message.success(this.$tc('SaveSuccess'))
      })
    },
    onCreate(type) {
      this.dataztree.hideRMenu()
      this.createDialogVisible = true
      this.createType = type
    },
    doCreate(name) {
      const parentNode = this.zTree.getSelectedNodes()[0]
      if (!parentNode) {
        return
      }
      const parentId = parentNode.isParent ? parentNode.id : parentNode.pId
      const req = {
        key: parentId,
        is_directory: this.createType === 'directory',
        name: name
      }
      this.$axios.post(`/api/v1/ops/playbook/${this.object.id}/file/`, req).then(data => {
        this.refreshTree()
      })
    },
    onDelete() {
      this.dataztree.hideRMenu()
      const node = this.zTree.getSelectedNodes()[0]
      if (!node) {
        return
      }
      this.$confirm(this.$tc('DeleteConfirmMessage'), this.$tc('Delete'), {
        confirmButtonText: this.$tc('Confirm'),
        cancelButtonText: this.$tc('Cancel'),
        type: 'warning'
      }).then(() => {
        this.$axios.delete(`/api/v1/ops/playbook/${this.object.id}/file/?key=${node.id}`).then(() => {
          if (!node.isParent) {
            this.remoteTab(node.id)
          }
          this.refreshTree()
          this.$message({
            type: 'success',
            message: this.$tc('DeleteSuccess')
          })
        })
      })
    },
    onRename() {
      this.dataztree.hideRMenu()
      const node = this.zTree.getSelectedNodes()[0]
      if (!node) {
        return
      }
      this.zTree.editName(node)
    },
    onOpenEditor(node) {
      this.$set(this.openedEditor, node.id,
        { key: node.id, name: node.name, originValue: '', value: '' })
      this.activeEditorId = node.id
      this.getFileContent(node.id)
    },
    onCloseEditor(key) {
      const editor = this.openedEditor[key]
      let text = ''
      if (this.hasChange(editor)) {
        text = this.$tc('CloseConfirmMessage')
      } else {
        this.remoteTab(key)
        return
      }
      this.$confirm(text, this.$tc('CloseConfirm'), {
        confirmButtonText: this.$tc('Confirm'),
        cancelButtonText: this.$tc('Cancel'),
        type: 'warning'
      }).then(() => {
        this.closing = true
        this.onSave()
      }).catch(() => {
        this.remoteTab(key)
      })
    },
    remoteTab(key) {
      this.$delete(this.openedEditor, key)
      const keys = Object.keys(this.openedEditor)
      if (keys.length !== 0) {
        this.activeEditorId = keys[keys.length - 1]
      }
    },
    getFileContent(key) {
      this.$axios.get(`/api/v1/ops/playbook/${this.object.id}/file/?key=${key}`).then((res) => {
        this.openedEditor[key].value = res.content
        this.openedEditor[key].originValue = res.content
      })
    },
    tabLabel(editor) {
      if (this.hasChange(editor)) {
        return (editor.key + ' M').replace('root/', '')
      }
      return editor.key.replace('root/', '')
    },
    hasChange(editor) {
      return editor.value !== editor.originValue
    },
    setVariable(variables) {
      if (this.disableEdit) {
        return
      }
      this.$axios.patch(`/api/v1/ops/playbooks/${this.object.id}/`,
        { variable: variables }).catch(err => {
        this.$message.error(this.$tc('UpdateErrorMsg') + ' ' + err)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.mini-button {
  width: 12px;
  float: right;
  text-align: center;
  padding: 5px 0;
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: #FFFFFF;
  border-radius: 2px;
}

.workspace-tab {
  ::v-deep .el-tabs__header {
    margin: 0 0 15px 30px !important;
  }
}

.el-tree {
  background-color: inherit !important;
}

.mini {
  margin-right: 5px;
  width: 12px !important;
}

.auto-data-zTree {
  overflow: auto;
  /*border-right: solid 1px red;*/
}

.vue-codemirror-wrap ::v-deep .CodeMirror {
  width: 600px;
  height: 100px;
  border: 1px solid #eee;
}

.tree-box {
  margin-right: 2px;
  border: 1px solid #e0e0e0;
}

.output {
  padding-left: 30px;
  background-color: rgb(247 247 247);
  border: solid 1px #f3f3f3;;
}

.status_success {
  color: var(--color-success);
}

.status_warning {
  color: var(--color-warning);
}

.status_danger {
  color: var(--color-danger);
}

.rmenu {
  font-size: 12px;
  padding: 0 16px;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #606266;
  height: 24px;
  line-height: 24px;
  box-sizing: border-box;
  cursor: pointer;
}
</style>

<template>
  <GenericDetailPage :active-menu.sync="config.activeMenu" :object.sync="group" v-bind="config" v-on="$listeners">
    <keep-alive>
      <component :is="config.activeMenu" :object="group" />
    </keep-alive>
  </GenericDetailPage>
</template>

<script>
import { GenericDetailPage } from '@/layout/components'
import GroupInfo from './GroupInfo'
import GroupUser from './GroupUser'

export default {
  components: {
    GenericDetailPage,
    GroupInfo,
    GroupUser
  },
  data() {
    return {
      group: { name: '', comment: '', users: [] },
      config: {
        url: '/api/v1/users/groups/',
        activeMenu: 'GroupInfo',
        submenu: [
          {
            title: this.$t('Basic'),
            name: 'GroupInfo'
          },
          {
            title: this.$t('UserList'),
            name: 'GroupUser'
          }
        ]
      }
    }
  },
  methods: {
    handleTabClick(tab) {
      this.$log.debug('Current nav is: ', this.config.activeMenu)
    }
  }
}
</script>

<style lang='scss' scoped>
::v-deep table.CardTable {
  table-layout: auto !important;
}
</style>

<template>
  <GenericDetailPage
    :active-menu.sync="config.activeMenu"
    :object.sync="user"
    v-bind="config"
    v-on="$listeners"
  >
    <keep-alive>
      <component :is="config.activeMenu" :object="user" />
    </keep-alive>
  </GenericDetailPage>
</template>

<script>
import { GenericDetailPage } from '@/layout/components'

import TransactionInfo from './TransactionInfo.vue'

export default {
  components: {
    TransactionInfo,
    GenericDetailPage
  },
  data() {
    return {
      user: {},
      config: {
        url: '/api/v1/finances/transactions/',
        activeMenu: 'TransactionInfo',
        actions: {
          canUpdate: () => {
            return this.$hasPerm('finances.change_transaction')
          }
        },
        submenu: [
          {
            title: this.$t('Basic'),
            name: 'TransactionInfo'
          }
        ]
      }
    }
  },
  computed: {
  },
  methods: {
  }
}
</script>

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
import { mapGetters } from 'vuex'
import { GenericDetailPage } from '@/layout/components'

import UserInfo from './UserInfo'

export default {
  components: {
    UserInfo,
    GenericDetailPage
  },
  data() {
    return {
      user: { name: '', username: '', email: '', comment: '' },
      config: {
        url: '/api/v1/users/users',
        activeMenu: 'UserInfo',
        actions: {
          canUpdate: () => {
            return this.$hasPerm('users.change_user') &&
              !(!this.currentUserIsSuperAdmin && this.user['is_superuser'])
          }
        },
        submenu: [
          {
            title: this.$t('Basic'),
            name: 'UserInfo'
          }
        ]
      }
    }
  },
  computed: {
    ...mapGetters([
      'currentUserIsSuperAdmin'
    ])
  },
  methods: {
    handleTabClick(tab) {
      this.$log.debug('Current nav is: ', this.config.activeMenu)
    }
  }
}
</script>

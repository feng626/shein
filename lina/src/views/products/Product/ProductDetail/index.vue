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

import ProductInfo from './ProductInfo.vue'

export default {
  components: {
    ProductInfo,
    GenericDetailPage
  },
  data() {
    return {
      user: {},
      config: {
        url: '/api/v1/products/products/',
        activeMenu: 'ProductInfo',
        actions: {
          canUpdate: () => {
            return this.$hasPerm('products.change_product')
          }
        },
        submenu: [
          {
            title: this.$t('Basic'),
            name: 'ProductInfo'
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

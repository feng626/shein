<template>
  <GenericCreateUpdatePage
    v-if="!loading"
    class="user-create-update"
    v-bind="$data"
    v-on="$listeners"
  />
</template>

<script>
import { GenericCreateUpdatePage } from '@/layout/components'

export default {
  components: {
    GenericCreateUpdatePage
  },
  data() {
    return {
      loading: true,
      initial: {
        need_update_password: true,
        system_roles: [],
        org_roles: []
      },
      user: {
        'can_public_key_auth': false
      },
      fields: [
        [this.$t('Basic'), ['name', 'spu', 'type', 'skc', 'sku', 'price']],
        [this.$t('Other'), ['avatar_url', 'number', 'comment']]
      ],
      url: '/api/v1/products/products/',
      fieldsMeta: {
      },
      submitMethod() {
        const params = this.$route.params
        if (params.id) {
          return 'put'
        } else {
          return 'post'
        }
      },
      cleanFormValue(value) {
        return value
      }
    }
  },
  computed: {
  },
  async mounted() {
    this.loading = false
  },
  methods: {
  }
}
</script>

<style lang="scss" scoped>
.user-create-update ::v-deep .el-form-item-need_update_password {
  margin-top: -10px;

  .el-form-item__content label {
    line-height: 30px;
  }
}

</style>

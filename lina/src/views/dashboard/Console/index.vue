<template>
  <Page>
    <div v-if="this.$hasPerm('rbac.view_console')">
      <Announcement />
    </div>
    <Page403 v-else />
  </Page>
</template>

<script>
import { Announcement } from '@/components'
import { Page } from '@/layout/components'
import Page403 from '@/views/403'

export default {
  name: 'Dashboard',
  components: {
    Page,
    Announcement,
    Page403
  },
  data() {
    return {}
  }
}
</script>

<style lang="scss" scoped>
</style>

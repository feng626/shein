<template>
  <TwoCol>
    <template>
      <AutoDetailCard
        :fields="detailFields"
        :formatters="detailFormatters"
        :object="object"
        :url="url"
      />
    </template>
  </TwoCol>
</template>

<script>
import AutoDetailCard from '@/components/Cards/DetailCard/auto'
import TwoCol from '@/layout/components/Page/TwoColPage.vue'

export default {
  name: 'ProductInfo',
  components: {
    TwoCol,
    AutoDetailCard
  },
  props: {
    object: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      url: `/api/v1/products/products/${this.object.id}`,
      detailFormatters: {
      },
      detailFields: [
        {
          key: '',
          formatter: () => {
            return <img src={this.object.avatar_url} alt='' height='50'/>
          }
        },
        'id', 'name', 'spu', 'type', 'skc',
        'sku', 'number', 'avatar_url', 'price'
      ]
    }
  },
  computed: {},
  watch: {
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
.mfa-setting ::v-deep .el-slider__runway {
  margin-top: 0;
  margin-bottom: 0;
}

.detail-right-quick-actions {
  display: flex;

  & > div {
    margin-right: 20px;
    width: 350px;
  }

  & > div:last-child {
    margin-right: 0; /* 清除最后一个元素的多余间距 */
  }
}

</style>

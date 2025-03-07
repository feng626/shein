import i18n from '@/i18n/i18n'
import empty from '@/layout/empty'

export default [
  {
    path: 'products',
    component: empty, // Parent router-view
    redirect: '',
    meta: {
      permissions: ['products.view_product'],
      expanded: true,
      icon: 'assets'
    },
    children: [
      {
        path: '',
        component: () => import('@/views/products/Product/ProductList.vue'), // Parent router-view
        name: 'ProductList',
        meta: {
          title: i18n.t('ProductList')
        }
      },
      {
        path: 'create',
        component: () => import('@/views/products/Product/ProductCreateUpdate.vue'), // Parent router-view
        name: 'ProductCreate',
        hidden: true,
        meta: {
          title: i18n.t('ProductCreate'),
          action: 'create'
        }
      },
      {
        path: ':id/update',
        component: () => import('@/views/products/Product/ProductCreateUpdate.vue'), // Parent router-view
        name: 'ProductUpdate',
        hidden: true,
        meta: {
          title: i18n.t('ProductUpdate'),
          action: 'update'
        }
      },
      {
        path: ':id',
        component: () => import('@/views/products/Product/ProductDetail'), // Parent router-view
        name: 'ProductDetail',
        hidden: true,
        meta: { title: i18n.t('ProductDetail') }
      }
    ]
  }
]

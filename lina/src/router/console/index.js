import Layout from '@/layout/index'
import i18n from '@/i18n/i18n'
import empty from '@/layout/empty'
import store from '@/store'

import UsersMenu from './users'
import ProductsMenu from './products'
import FinancesMenu from './finances'

export default {
  path: '/console',
  component: Layout,
  name: 'console',
  redirect: '/console/dashboard',
  meta: {
    title: i18n.t('Console'),
    icon: 'console',
    view: 'console',
    type: 'view',
    showNavSwitcher: () => {
      return store.getters.consoleOrgs.length > 0
    },
    permissions: []
  },
  children: [
    {
      path: '/console/dashboard',
      component: () => import('@/views/dashboard/Console/index.vue'),
      name: 'AdminDashboard',
      meta: {
        icon: 'dashboard',
        title: i18n.t('Dashboard'),
        permissions: []
      }
    },
    {
      path: '/console/users',
      component: empty,
      name: 'Users',
      meta: {
        title: i18n.t('MenuUsers'),
        icon: 'users'
      },
      children: UsersMenu
    },
    {
      path: '/console/products',
      component: empty,
      name: 'Products',
      meta: {
        title: i18n.t('ProductsMenu'),
        icon: 'assets'
      },
      children: ProductsMenu
    },
    {
      path: '/console/finances',
      component: empty,
      name: 'Finances',
      meta: {
        title: i18n.t('FinancesMenu'),
        icon: 'ticket-list'
      },
      children: FinancesMenu
    }
  ]
}


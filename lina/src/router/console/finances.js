import i18n from '@/i18n/i18n'
import empty from '@/layout/empty'

export default [
  {
    path: 'transaction',
    component: empty, // Parent router-view
    redirect: '',
    meta: {
      permissions: ['finances.view_transaction'],
      expanded: true,
      icon: 'ticket-list'
    },
    children: [
      {
        path: '',
        component: () => import('@/views/finances/Transaction/TransactionList.vue'), // Parent router-view
        name: 'TransactionList',
        meta: {
          title: i18n.t('TransactionList')
        }
      },
      {
        path: 'create',
        component: () => import('@/views/finances/Transaction/TransactionCreateUpdate.vue'), // Parent router-view
        name: 'TransactionCreate',
        hidden: true,
        meta: {
          title: i18n.t('TransactionCreate'),
          action: 'create'
        }
      },
      {
        path: ':id/update',
        component: () => import('@/views/finances/Transaction/TransactionCreateUpdate.vue'), // Parent router-view
        name: 'TransactionUpdate',
        hidden: true,
        meta: {
          title: i18n.t('TransactionUpdate'),
          action: 'update'
        }
      },
      {
        path: ':id',
        component: () => import('@/views/finances/Transaction/TransactionDetail'), // Parent router-view
        name: 'TransactionDetail',
        hidden: true,
        meta: { title: i18n.t('TransactionDetail') }
      }
    ]
  }
]

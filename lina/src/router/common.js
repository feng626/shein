import i18n from '@/i18n/i18n'

/**
 * admin and user routes
 * the routes that need to be dynamically loaded based on admin or user roles
 */
export default [
  {
    path: '/ops/celery/task/:id/log/',
    component: () => import('@/views/settings/Task/CeleryTaskLog'),
    name: 'CeleryTaskLog',
    hidden: true,
    meta: {
      title: i18n.t('CeleryTaskLog'),
      permissions: []
    }
  }
]

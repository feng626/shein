import i18n from '@/i18n/i18n'
import empty from '@/layout/empty'

const Setting = () => import('@/views/settings/index')
const globalSubmenu = () => import('@/layout/globalOrg.vue')

export default {
  path: '/settings',
  component: Setting,
  redirect: '/settings/basic',
  name: 'SystemSetting',
  meta: {
    title: i18n.t('Settings'),
    icon: 'system-setting',
    activeMenu: '/settings',
    view: 'settings',
    type: 'view',
    showNavSwitcher: false,
    showOrganization: false,
    permissions: ['settings.view_setting']
  },
  children: [
    {
      path: '/settings/basic',
      name: 'Basic',
      component: () => import('@/views/settings/Basic'),
      meta: {
        title: i18n.t('BasicSettings'),
        icon: 'basic',
        permissions: ['settings.view_setting']
      }
    },
    {
      path: '/settings/orgs',
      component: empty,
      redirect: '',
      meta: {
        app: 'orgs',
        resource: 'organization',
        permissions: ['orgs.view_organization'],
        licenseRequired: true
      },
      children: [
        {
          path: '',
          component: () => import('@/views/settings/Org/OrganizationList'),
          name: 'OrganizationList',
          meta: {
            title: i18n.t('OrganizationList'),
            icon: 'organization-set',
            permissions: ['orgs.view_organization']
          }
        },
        {
          path: 'create',
          component: () => import('@/views/settings/Org/OrganizationCreateUpdate'),
          name: 'OrganizationCreate',
          hidden: true,
          meta: {
            title: i18n.t('OrganizationCreate'),
            action: 'create',
            permissions: ['orgs.add_organization'],
            activeMenu: '/settings/orgs'
          }
        },
        {
          path: ':id/update',
          component: () => import('@/views/settings/Org/OrganizationCreateUpdate'),
          name: 'OrganizationUpdate',
          hidden: true,
          meta: {
            title: i18n.t('OrganizationUpdate'),
            action: 'update',
            permissions: ['orgs.change_organization'],
            activeMenu: '/settings/orgs'
          }
        },
        {
          path: ':id',
          component: () => import('@/views/settings/Org/OrganizationDetail/index'),
          name: 'OrganizationDetail',
          hidden: true,
          meta: {
            title: i18n.t('OrganizationDetail'),
            permissions: ['orgs.view_organization']
          }
        }
      ]
    },
    {
      path: '/settings/roles',
      component: globalSubmenu,
      redirect: '',
      meta: {
        permissions: ['rbac.view_orgrole | rbac.view_systemrole'],
        app: 'rbac',
        disableOrgsChange: true,
        licenseRequired: true,
        icon: 'role'
      },
      children: [
        {
          path: '',
          component: () => import('@/views/users/Role/RoleList/index'),
          name: 'RoleList',
          meta: {
            title: i18n.t('RoleList'),
            app: 'rbac',
            permissions: ['rbac.view_orgrole | rbac.view_systemrole']
          }
        },
        {
          path: 'create',
          component: () => import('@/views/users/Role/RoleCreateUpdate'),
          name: 'RoleCreate',
          hidden: true,
          meta: {
            title: i18n.t('RoleCreate'),
            permissions: [],
            app: 'rbac',
            resource: 'role'
          }
        },
        {
          path: ':id/update',
          component: () => import('@/views/users/Role/RoleCreateUpdate'),
          name: 'RoleUpdate',
          hidden: true,
          meta: {
            title: i18n.t('RoleUpdate'),
            app: 'rbac',
            permissions: []
          }
        },
        {
          path: ':id',
          component: () => import('@/views/users/Role/RoleDetail/index'),
          name: 'RoleDetail',
          hidden: true,
          meta: {
            title: i18n.t('RoleDetail'),
            app: 'rbac',
            resource: 'role',
            permissions: []
          }
        }
      ]
    },
    {
      path: '/settings/notification',
      name: 'Msg',
      component: () => import('@/views/settings/Msg'),
      meta: {
        title: i18n.t('Notifications'),
        icon: 'remind',
        permissions: ['settings.change_email | settings.change_sms | settings.change_systemmsgsubscription']
      }
    },
    {
      path: '/settings/auth',
      name: 'Auth',
      component: () => import('@/views/settings/Auth'),
      meta: {
        title: i18n.t('Auth'),
        icon: 'attestation',
        permissions: ['settings.change_auth']
      }
    },
    {
      path: '/settings/security',
      name: 'Security',
      component: () => import('@/views/settings/Security'),
      meta: {
        title: i18n.t('Security'),
        icon: 'security',
        permissions: ['settings.change_security']
      }
    },
    {
      path: '/settings/interface',
      name: 'Interface',
      component: () => import('@/views/settings/Interface'),
      meta: {
        title: i18n.t('InterfaceSettings'),
        icon: 'face',
        licenseRequired: true,
        permissions: ['settings.change_interface']
      }
    },
    {
      path: '/settings/tools',
      name: 'Tools',
      component: () => import('@/views/settings/Tool'),
      meta: {
        title: i18n.t('SystemTools'),
        icon: 'tools',
        permissions: ['settings.view_setting']
      }
    },
    {
      path: '/settings/license',
      name: 'License',
      component: () => import('@/views/settings/License'),
      meta: {
        title: i18n.t('License'),
        icon: 'license',
        permissions: ['settings.change_license']
      }
    }
  ]
}


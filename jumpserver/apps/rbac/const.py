from django.db import models
from django.utils.translation import gettext_lazy as _


class Scope(models.TextChoices):
    system = 'system', _('System')
    org = 'org', _('Organization')


exclude_permissions = (
    # ('App', 'Model', 'Action', 'Resource') Model 和 Resource 可能不同
    # users.add_user
    ('auth', '*', '*', '*'),
    ('captcha', '*', '*', '*'),
    ('contenttypes', '*', '*', '*'),
    ('django_cas_ng', '*', '*', '*'),
    ('django_celery_beat', '*', '*', '*'),
    ('jms_oidc_rp', '*', '*', '*'),
    ('admin', '*', '*', '*'),
    ('notifications', '*', '*', '*'),
    ('common', 'setting', '*', '*'),

    ('authentication', 'privatetoken', '*', '*'),
    ('authentication', 'connectiontoken', 'delete,change', 'connectiontoken'),
    ('authentication', 'connectiontoken', 'view', 'connectiontokensecret'),
    ('authentication', 'ssotoken', '*', '*'),
    ('authentication', 'superconnectiontoken', 'change,delete', 'superconnectiontoken'),
    ('authentication', 'temptoken', 'delete', 'temptoken'),
    ('users', 'userpasswordhistory', '*', '*'),
    ('users', 'usersession', '*', '*'),

    ('rbac', 'contenttype', 'add,change,delete', '*'),
    ('rbac', 'permission', 'add,delete,change', 'permission'),
    ('rbac', 'rolebinding', '*', '*'),
    ('rbac', 'systemrolebinding', 'change', 'systemrolebinding'),
    ('rbac', 'orgrolebinding', 'change', 'orgrolebinding'),
    ('rbac', 'menupermission', '*', 'menupermission'),
    ('ops', 'celerytask', 'add,change,delete', 'celerytask'),
    ('ops', 'celerytaskexecution', 'add,change,delete', 'celerytaskexecution'),
    ('orgs', 'organizationmember', '*', '*'),
    ('settings', 'setting', 'add,change,delete', 'setting'),
    ('xpack', 'interface', '*', '*'),
    ('xpack', 'license', '*', '*'),
    ('common', 'permission', 'add,delete,view,change', 'permission'),
)

only_system_permissions = (
    ('users', 'user', 'delete', 'user'),
    ('rbac', 'role', 'delete,add,change', 'role'),
    ('rbac', 'systemrole', '*', '*'),
    ('rbac', 'rolebinding', '*', '*'),
    ('rbac', 'systemrolebinding', '*', '*'),
    ('rbac', 'orgrole', 'delete,add,change', 'orgrole'),
    ('orgs', 'organization', '*', '*'),
    ('xpack', 'license', '*', '*'),
    ('settings', 'setting', '*', '*'),
    ('ops', 'celerytask', 'view', 'taskmonitor'),
    ('authentication', 'accesskey', '*', '*'),
    ('authentication', 'superconnectiontoken', '*', '*'),
    ('authentication', 'temptoken', '*', '*'),
    ('authentication', 'passkey', '*', '*'),
    ('orgs', 'organization', 'view', 'rootorg'),
)

only_org_permissions = (
)

system_exclude_permissions = list(exclude_permissions) + list(only_org_permissions)
org_exclude_permissions = list(exclude_permissions) + list(only_system_permissions)

import time

from django.conf import settings
from rest_framework import permissions

from authentication.const import ConfirmType
from common.exceptions import UserConfirmRequired


class UserConfirmation(permissions.BasePermission):
    ttl = 60 * 5
    min_level = 1
    confirm_type = 'relogin'

    def has_permission(self, request, view):
        if not settings.SECURITY_VIEW_AUTH_NEED_MFA:
            return True

        confirm_level = request.session.get('CONFIRM_LEVEL')
        confirm_time = request.session.get('CONFIRM_TIME')
        ttl = self.get_ttl()
        if not confirm_level or not confirm_time or \
                confirm_level < self.min_level or \
                confirm_time < time.time() - ttl:
            raise UserConfirmRequired(code=self.confirm_type)
        return True

    def get_ttl(self):
        if self.confirm_type == ConfirmType.MFA:
            ttl = settings.SECURITY_MFA_VERIFY_TTL
        else:
            ttl = self.ttl
        return ttl

    @classmethod
    def require(cls, confirm_type=ConfirmType.RELOGIN, ttl=60 * 5):
        min_level = ConfirmType.values.index(confirm_type) + 1
        name = 'UserConfirmationLevel{}TTL{}'.format(min_level, ttl)
        return type(name, (cls,), {'min_level': min_level, 'ttl': ttl, 'confirm_type': confirm_type})

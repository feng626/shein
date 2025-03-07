from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from common.exceptions import JMSException
from . import const


class NeedMoreInfoError(Exception):
    error = ''
    msg = ''

    def __init__(self, error='', msg=''):
        if error:
            self.error = error
        if msg:
            self.msg = msg

    def as_data(self):
        return {
            'error': self.error,
            'msg': self.msg,
        }


class NeedRedirectError(JMSException):
    def __init__(self, url, *args, **kwargs):
        self.url = url


class MFARequiredError(NeedMoreInfoError):
    msg = const.mfa_required_msg
    error = 'mfa_required'

    def __init__(self, error='', msg='', mfa_types=()):
        super().__init__(error=error, msg=msg)
        self.choices = mfa_types

    def as_data(self):
        return {
            'error': self.error,
            'msg': self.msg,
            'data': {
                'choices': self.choices,
                'url': reverse('api-auth:mfa-challenge')
            }
        }


class PasswordTooSimple(NeedRedirectError):
    default_code = 'passwd_too_simple'
    default_detail = _('Your password is too simple, please change it for security')

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)


class PasswordNeedUpdate(NeedRedirectError):
    default_code = 'passwd_need_update'
    default_detail = _('You should to change your password before login')

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)


class PasswordRequireResetError(NeedRedirectError):
    default_code = 'passwd_has_expired'
    default_detail = _('Your password has expired, please reset before logging in')

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)


class MFAUnsetError(NeedRedirectError):
    error = const.reason_mfa_unset
    msg = const.mfa_unset_msg

    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)

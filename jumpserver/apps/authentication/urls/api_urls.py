# coding:utf-8
#
from django.urls import path
from rest_framework.routers import DefaultRouter

from .. import api
from ..backends.passkey.urls import urlpatterns as passkey_urlpatterns

app_name = 'authentication'
router = DefaultRouter()
router.register('sso', api.SSOViewSet, 'sso')
router.register('temp-tokens', api.TempTokenViewSet, 'temp-token')
router.register('confirm', api.UserConfirmationViewSet, 'confirm')
router.register('ssh-key', api.SSHkeyViewSet, 'ssh-key')

urlpatterns = [
    path('<str:backend>/qr/unbind/', api.QRUnBindForUserApi.as_view(), name='qr-unbind'),
    path('<str:backend>/qr/unbind/<uuid:user_id>/', api.QRUnBindForAdminApi.as_view(), name='qr-unbind-for-admin'),

    path('feishu/event/subscription/callback/', api.FeiShuEventSubscriptionCallback.as_view(),
         name='feishu-event-subscription-callback'),

    path('lark/event/subscription/callback/', api.LarkEventSubscriptionCallback.as_view(),
         name='lark-event-subscription-callback'),

    path('auth/', api.TokenCreateApi.as_view(), name='user-auth'),
    path('confirm-oauth/', api.ConfirmBindORUNBindOAuth.as_view(), name='confirm-oauth'),
    path('tokens/', api.TokenCreateApi.as_view(), name='auth-token'),
    path('mfa/verify/', api.MFAChallengeVerifyApi.as_view(), name='mfa-verify'),
    path('mfa/challenge/', api.MFAChallengeVerifyApi.as_view(), name='mfa-challenge'),
    path('mfa/select/', api.MFASendCodeApi.as_view(), name='mfa-select'),
    path('mfa/send-code/', api.MFASendCodeApi.as_view(), name='mfa-send-code'),
    path('password/reset-code/', api.UserResetPasswordSendCodeApi.as_view(), name='reset-password-code'),
    path('password/verify/', api.UserPasswordVerifyApi.as_view(), name='user-password-verify'),
    path('user-session/', api.UserSessionApi.as_view(), name='user-session'),
]

urlpatterns += router.urls + passkey_urlpatterns

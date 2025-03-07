import uuid

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.serializers.fields import EncryptedField
from common.utils import date_expired_default

__all__ = [
    'AnnouncementSettingSerializer', 'OpsSettingSerializer', 'AmazonSMSerializer',
]


class AnnouncementSerializer(serializers.Serializer):
    ID = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    SUBJECT = serializers.CharField(required=True, max_length=1024, label=_("Subject"))
    CONTENT = serializers.CharField(label=_("Content"))
    LINK = serializers.URLField(
        required=False, allow_null=True, allow_blank=True,
        label=_("More Link"), default='',
    )
    DATE_START = serializers.DateTimeField(default=timezone.now, label=_("Date start"))
    DATE_END = serializers.DateTimeField(default=date_expired_default, label=_("Date end"))

    def to_representation(self, instance):
        defaults = {'ID': '', 'SUBJECT': '', 'CONTENT': '', 'LINK': '', 'ENABLED': False}
        data = {**defaults, **instance}
        return super().to_representation(data)

    def to_internal_value(self, data):
        data['ID'] = str(uuid.uuid4())
        return super().to_internal_value(data)


class AnnouncementSettingSerializer(serializers.Serializer):
    PREFIX_TITLE = _('Announcement')

    ANNOUNCEMENT_ENABLED = serializers.BooleanField(label=_('Announcement'), default=True)
    ANNOUNCEMENT = AnnouncementSerializer(label=_("Announcement"))


class AmazonSMSerializer(serializers.Serializer):
    PREFIX_TITLE = _('Amazon Secrets Manager')
    VAULT_AWS_REGION_NAME = serializers.CharField(
        max_length=256, required=True, label=_('Region')
    )
    VAULT_AWS_ACCESS_KEY_ID = serializers.CharField(
        max_length=1024, required=True, label=_('Access key ID')
    )
    VAULT_AWS_ACCESS_SECRET_KEY = EncryptedField(
        max_length=1024, required=False, allow_blank=True,
        label=_('Access key secret'), default=''
    )


class OpsSettingSerializer(serializers.Serializer):
    PREFIX_TITLE = _('Feature')

    SECURITY_COMMAND_EXECUTION = serializers.BooleanField(
        required=False, label=_('Adhoc'),
        help_text=_('Allow users to execute batch commands in the Workbench - Job Center - Adhoc')
    )
    SECURITY_COMMAND_BLACKLIST = serializers.ListField(
        child=serializers.CharField(max_length=1024, ),
        label=_('Command blacklist'),
        help_text=_("Command blacklist in Adhoc")
    )

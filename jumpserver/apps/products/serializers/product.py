# -*- coding: utf-8 -*-
#
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import Product

__all__ = ['ProductSerializer', 'ImportExcelSerializer']


class ProductSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'spu', 'type', 'skc',
            'sku', 'cost', 'number', 'avatar_url', 'price'
        ]


class ImportExcelSerializer(serializers.Serializer):
    file = serializers.FileField(label=_('Excel File'))

    @staticmethod
    def validate_file(file):
        # openpyxl
        if not file.name.endswith(('.xlsx',)):
            raise serializers.ValidationError(_('Only Excel files are allowed.'))
        return file

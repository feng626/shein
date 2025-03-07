# -*- coding: utf-8 -*-
#
from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import Transaction

__all__ = ['TransactionListSerializer', 'TransactionSerializer']


class TransactionListSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'name', 'amount', 'state', 'price', 'product', 'datetime'
        ]


class TransactionSerializer(TransactionListSerializer):
    class Meta:
        model = Transaction
        fields = TransactionListSerializer.Meta.fields + [
            'comment'
        ]

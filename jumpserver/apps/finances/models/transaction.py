# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from orgs.mixins.models import JMSOrgBaseModel

__all__ = ['Transaction']


class Transaction(JMSOrgBaseModel):
    name = models.CharField(max_length=1024, verbose_name=_('Name'))
    amount = models.IntegerField(verbose_name=_('Amount'))
    state = models.CharField(max_length=128, verbose_name=_('State'))
    business_number = models.CharField(max_length=128, verbose_name=_('Business Number'), unique=True)
    source_number = models.CharField(max_length=128, verbose_name=_('Source Number'))
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Price'))
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name=_('Product'))
    datetime = models.DateTimeField(default=timezone.now, verbose_name=_("Bill creation time"), db_index=True)

    # 货号 SKC 属性集 活动信息 台账添加日期 预计结算日期 实际日期

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Transaction')

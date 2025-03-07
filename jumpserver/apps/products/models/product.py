# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from orgs.mixins.models import JMSOrgBaseModel

__all__ = ['Product']


class Product(JMSOrgBaseModel):
    name = models.CharField(max_length=1024, verbose_name=_('Name'))
    spu = models.CharField(max_length=128, verbose_name='SPU')
    type = models.CharField(max_length=128, verbose_name=_('Type'))
    skc = models.CharField(max_length=128, verbose_name='SKC')
    sku = models.CharField(max_length=128, unique=True, verbose_name='SKU')
    number = models.CharField(max_length=128, verbose_name=_('Number'))
    avatar_url = models.URLField(max_length=1024, verbose_name=_('Avatar URL'))
    cost = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Cost'))
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Price'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')

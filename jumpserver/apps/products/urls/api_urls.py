#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'users'

router = BulkRouter()
router.register(r'products', api.ProductViewSet, 'product')

urlpatterns = []
urlpatterns += router.urls

# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = "ops"

router = DefaultRouter()
bulk_router = BulkRouter()

router.register(r'celery/period-tasks', api.CeleryPeriodTaskViewSet, 'celery-period-task')

router.register(r'tasks', api.CeleryTaskViewSet, 'task')
router.register(r'task-executions', api.CeleryTaskExecutionViewSet, 'task-executions')

urlpatterns = [
    path('celery/task/<uuid:name>/task-execution/<uuid:pk>/log/', api.CeleryTaskExecutionLogApi.as_view(),
         name='celery-task-execution-log'),
    path('celery/task/<uuid:name>/task-execution/<uuid:pk>/result/', api.CeleryResultApi.as_view(),
         name='celery-task-execution-result'),

]

urlpatterns += (router.urls + bulk_router.urls)

# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals

import os

import private_storage.urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.i18n import JavaScriptCatalog

from . import views

api_v1 = [
    path('users/', include('users.urls.api_urls', namespace='api-users')),
    path('products/', include('products.urls.api_urls', namespace='api-products')),
    path('finances/', include('finances.urls.api_urls', namespace='api-finances')),
    path('ops/', include('ops.urls.api_urls', namespace='api-ops')),
    path('orgs/', include('orgs.urls.api_urls', namespace='api-orgs')),
    path('settings/', include('settings.urls.api_urls', namespace='api-settings')),
    path('authentication/', include('authentication.urls.api_urls', namespace='api-auth')),
    path('common/', include('common.urls.api_urls', namespace='api-common')),
    path('notifications/', include('notifications.urls.api_urls', namespace='api-notifications')),
    path('rbac/', include('rbac.urls.api_urls', namespace='api-rbac')),
]

app_view_patterns = [
    path('auth/', include('authentication.urls.view_urls'), name='auth'),
    path('ops/', include('ops.urls.view_urls'), name='ops'),
    path('common/', include('common.urls.view_urls'), name='common'),
    re_path(r'flower/(?P<path>.*)', views.celery_flower_view, name='flower-view'),
    path('download/', views.ResourceDownload.as_view(), name='download'),
    path('i18n/<str:lang>/', views.I18NView.as_view(), name='i18n-switch'),
]

if settings.XPACK_ENABLED:
    api_v1.append(
        path('xpack/', include('xpack.urls.api_urls', namespace='api-xpack'))
    )

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('api/v1/', include(api_v1)),
    # External apps url
    path('core/auth/captcha/', include('captcha.urls')),
    path('core/', include(app_view_patterns)),
]

# 静态文件处理路由
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    # Protect media
    path('media/', include(private_storage.urls)),
]
if settings.DEBUG:
    urlpatterns += static('/luna/', document_root=(settings.DATA_DIR + '/luna'))
    urlpatterns += static('/ui/', document_root=(settings.DATA_DIR + '/lina'))
else:
    urlpatterns += path('ui/', views.UIView.as_view()),

# js i18n 路由文件
urlpatterns += [
    path('core/jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# docs 路由
urlpatterns += [
    re_path('^api/swagger(?P<format>\.json|\.yaml)$',
            views.get_swagger_view().without_ui(cache_timeout=1), name='schema-json'),
    re_path('api/docs/?', views.get_swagger_view().with_ui('swagger', cache_timeout=1), name="docs"),
    re_path('api/redoc/?', views.get_swagger_view().with_ui('redoc', cache_timeout=1), name='redoc'),
]

if os.environ.get('DEBUG_TOOLBAR', False):
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

handler404 = 'jumpserver.views.handler404'
handler500 = 'jumpserver.views.handler500'

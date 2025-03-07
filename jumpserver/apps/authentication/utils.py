# -*- coding: utf-8 -*-
#
from urllib.parse import urljoin, urlparse

from django.conf import settings

from common.utils import get_logger, get_object_or_none
from users.models import User

logger = get_logger(__file__)


def build_absolute_uri(request, path=None):
    """ Build absolute redirect """
    if path is None:
        path = '/'
    site_url = urlparse(settings.SITE_URL)
    scheme = site_url.scheme or request.scheme
    host = request.get_host()
    url = f'{scheme}://{host}'
    redirect_uri = urljoin(url, path)
    return redirect_uri


def build_absolute_uri_for_oidc(request, path=None):
    """ Build absolute redirect uri for OIDC """
    if path is None:
        path = '/'
    if settings.BASE_SITE_URL:
        # OIDC 专用配置项
        redirect_uri = urljoin(settings.BASE_SITE_URL, path)
        return redirect_uri
    return build_absolute_uri(request, path=path)


def check_user_property_is_correct(username, **properties):
    user = get_object_or_none(User, username=username)
    for attr, value in properties.items():
        if getattr(user, attr, None) != value:
            user = None
            break
    return user

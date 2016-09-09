# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .administration import urls as admin_urls
from .ticket import urls as ticket_urls


urlpatterns = [
    url(r'^', include(ticket_urls)),

    url(r'^admin/', include(admin_urls)),
]

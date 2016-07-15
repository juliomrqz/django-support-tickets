# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .ticket import urls as ticket_urls


urlpatterns = [
    url(r'^tickets/', include(ticket_urls)),
]

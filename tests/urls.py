# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from support_tickets.urls import urlpatterns as support_tickets_urls

urlpatterns = [
    url(r'^', include(support_tickets_urls, namespace='support_tickets')),
]

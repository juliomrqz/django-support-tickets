# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r"^create/$",
        view=views.TicketCreateView.as_view(),
        name="ticket_create",
    ),
]

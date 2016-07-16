# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r"^create/$",
        view=views.TicketCreateView.as_view(),
        name="ticket_create",
    ),

    url(
        regex=r"^$",
        view=views.TicketListView.as_view(),
        name="ticket_list",
    ),

    url(
        regex=r"^(?P<pk>\d+)/$",
        view=views.TicketDetailView.as_view(),
        name="ticket_detail",
    ),
]

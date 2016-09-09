# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [

    url(
        regex=r"^$",
        view=views.AdminHomeView.as_view(),
        name="admin_home",
    ),

    url(
        regex=r"^ticket/create/$",
        view=views.AdminTicketCreateView.as_view(),
        name="admin_ticket_create",
    ),

    url(
        regex=r"^ticket/(?P<pk>\d+)/$",
        view=views.AdminTicketDetailView.as_view(),
        name="admin_ticket_detail",
    ),

    url(
        regex=r"^ticket/(?P<pk>\d+)/delete/$",
        view=views.AdminTicketDeleteView.as_view(),
        name="admin_ticket_delete",
    ),

    url(
        regex=r"^ticket/(?P<pk>\d+)/close/$",
        view=views.AdminTicketCloseView.as_view(),
        name="admin_ticket_close",
    ),

    url(
        regex=r"^ticket/(?P<pk>\d+)/open/$",
        view=views.AdminTicketOpenView.as_view(),
        name="admin_ticket_open",
    ),

    url(
        regex=r"^ticket/(?P<pk>\d+)/properties/$",
        view=views.AdminTicketPropertiesUpdateView.as_view(),
        name="admin_ticket_properties_update",
    ),
]

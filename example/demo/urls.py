# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex="^$",
        view=views.HomeView.as_view(),
        name='home',
    ),
]

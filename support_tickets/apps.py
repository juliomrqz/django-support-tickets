# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SupportTicketsConfig(AppConfig):
    name = 'support_tickets'
    verbose_name = _("Support Tickets")

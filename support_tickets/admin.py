# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .category.admin import CategoryAdmin
from .ticket.admin import TicketAdmin

from .models import Category, Ticket

admin.site.register(Category, CategoryAdmin)
admin.site.register(Ticket, TicketAdmin)

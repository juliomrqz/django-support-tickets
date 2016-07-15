# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .attachment.admin import AttachmentAdmin
from .category.admin import CategoryAdmin
from .comment.admin import CommentAdmin
from .ticket.admin import TicketAdmin

from .models import Attachment, Category, Comment, Ticket

admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Ticket, TicketAdmin)

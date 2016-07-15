from __future__ import unicode_literals

from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = (
        'user',
        'ticket',
    )
    list_filter = ('created',)
    raw_id_fields = ('user', 'ticket',)
    search_fields = [
        'title',
        'user__first_name',
        'user__last_name',
        'user__username',
    ]

    def get_queryset(self, request):
        attachments = super(CommentAdmin, self).get_queryset(request)
        attachments = attachments.prefetch_related("user")

        return attachments

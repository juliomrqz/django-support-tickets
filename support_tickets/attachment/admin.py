from __future__ import unicode_literals

from django.contrib import admin


class AttachmentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = (
        'name',
        'file',
        'uploader',
        'comment',
        'created',
    )
    list_filter = ('created',)
    raw_id_fields = ('uploader', 'comment',)
    readonly_fields = ('name', 'size',)
    search_fields = [
        'title',
        'uploader__first_name',
        'uploader__last_name',
        'uploader__username',
    ]

    def get_queryset(self, request):
        attachments = super(AttachmentAdmin, self).get_queryset(request)
        attachments = attachments.prefetch_related("uploader")

        return attachments

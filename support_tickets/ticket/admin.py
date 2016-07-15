from __future__ import unicode_literals

from django.contrib import admin


class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = (
        'subject',
        'created',
        'submitter',
        'agent',
        'category',
        'status',
        'priority',
    )
    list_filter = ('created', 'status', 'priority')
    raw_id_fields = ('submitter', 'agent',)
    search_fields = [
        'subject',
        'submitter__first_name',
        'submitter__last_name',
        'submitter__username',
        'agent__first_name',
        'agent__last_name',
        'agent__username',
    ]

    def get_queryset(self, request):
        tickets = super(TicketAdmin, self).get_queryset(request)
        tickets = tickets.prefetch_related("submitter")
        tickets = tickets.prefetch_related("agent")
        tickets = tickets.prefetch_related("category")

        return tickets

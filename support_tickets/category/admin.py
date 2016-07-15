from __future__ import unicode_literals

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Category


class CategoryAdmin(TreeAdmin):
    date_hierarchy = 'created'
    list_display = (
        'title',
        'created',
        'default_agent',
    )
    list_filter = ('created',)
    raw_id_fields = ('default_agent',)
    readonly_fields = ('slug',)
    search_fields = [
        'title',
        'default_agent__first_name',
        'default_agent__last_name',
        'default_agent__username',
    ]

    form = movenodeform_factory(Category)

    def get_queryset(self, request):
        categories = super(CategoryAdmin, self).get_queryset(request)
        categories = categories.prefetch_related("default_agent")

        return categories

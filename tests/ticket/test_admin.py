#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-knowledgebase
------------

Tests for `django-knowledgebase` models module.
"""

from __future__ import absolute_import, unicode_literals

from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from support_tickets.admin import TicketAdmin
from support_tickets.base.choices import TICKET_STATUS
from support_tickets.models import Ticket

from ..mommy_recipes import user, category, ticket


class ModifiedTicketAdmin(TicketAdmin):

    def message_user(self, request, message):
        self.knowledgebase_message = message


class MockRequest(object):
    pass


class MockSuperUser(object):

    def has_perm(self, perm):
        return True


class AdminTicketTest(TestCase):

    def setUp(self):
        self.app_admin = ModifiedTicketAdmin(Ticket, AdminSite())
        self.request = MockRequest()
        self.request.user = MockSuperUser()

        self.user = user.make()
        self.category = category.make(
            author=self.user, _quantity=1
        )
        self.tickets = ticket.make(
            category=self.category[0],
            author=self.user,
            _quantity=3
        )
        self.tickets_published = ticket.make(
            category=self.category[0],
            author=self.user,
            status=TICKET_STATUS.published,
            _quantity=3
        )

    def test_default_fields(self):
        defaul_fields = ['author', 'category', 'content',
                         'markup', 'slug', 'status', 'tags',
                         'title']

        fields = sorted(
            list(self.app_admin.get_form(self.request).base_fields)
        )
        self.assertEqual(fields, defaul_fields)

        fields = sorted(list(self.app_admin.get_fields(self.request)))
        self.assertEqual(fields, defaul_fields)

        fields = sorted(
            list(self.app_admin.get_fields(self.request, self.tickets[0]))
        )
        self.assertEqual(fields, defaul_fields)

    def test_custom_display_fields(self):
        ticket = Ticket.objects.filter(pk=4)[0]

        self.assertEqual(
            self.app_admin.category_title(ticket),
            ticket.category.title
        )

    def test_make_draft_action(self):
        queryset = Ticket.objects.filter(pk=4)
        queryset_all = Ticket.objects.all()

        self.app_admin.make_draft(self.request, queryset)

        self.assertEqual(len(Ticket.objects.unpublished()), 4)
        self.assertEqual(
            self.app_admin.knowledgebase_message,
            '1 ticket was successfully marked as draft.'
        )

        self.app_admin.make_draft(self.request, queryset_all)

        self.assertEqual(len(Ticket.objects.unpublished()), 6)
        self.assertEqual(
            self.app_admin.knowledgebase_message,
            '6 tickets were successfully marked as draft.'
        )

    def test_make_published_action(self):
        queryset = Ticket.objects.filter(pk=1)
        queryset_all = Ticket.objects.all()

        self.app_admin.make_published(self.request, queryset)

        self.assertEqual(len(Ticket.objects.published()), 4)
        self.assertEqual(
            self.app_admin.knowledgebase_message,
            '1 ticket was successfully marked as published.'
        )

        self.app_admin.make_published(self.request, queryset_all)

        self.assertEqual(len(Ticket.objects.published()), 6)
        self.assertEqual(
            self.app_admin.knowledgebase_message,
            '6 tickets were successfully marked as published.'
        )

    def tearDown(self):
        pass

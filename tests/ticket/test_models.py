#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-knowledgebase
------------

Tests for `django-knowledgebase` models module.
"""

from __future__ import absolute_import, unicode_literals

from django_markup.templatetags.markup_tags import apply_markup

from support_tickets.base.choices import TICKET_STATUS
from support_tickets.models import Ticket
from ..tests import TicketCategorySetUpMixin


class TicketTest(TicketCategorySetUpMixin):

    def test_create_new_ticket(self):
        obj1 = self.tickets_one[2]
        obj1_tags_name = sorted(tuple(obj1.tags.names()))
        obj2 = self.custom_ticket[0]

        self.assertTrue(obj1.title)
        self.assertTrue(obj1.created)
        self.assertTrue(obj1.modified)

        self.assertEqual(obj1.title, str(obj1))
        self.assertEqual(obj1.title, 'Ticket3')
        self.assertEqual(obj1.author, self.user_one)
        self.assertEqual(obj1_tags_name, ['blue', 'green', 'red'])

        self.assertEqual(obj2.title, 'Custom Ticket')
        self.assertEqual(obj2.markup, 'markdown')
        self.assertEqual(obj2.content, '# Title')
        self.assertEqual(apply_markup(obj2.content, obj2.markup), '<h1>Title</h1>')

    def test_ticket_querysets(self):
        self.assertEqual(len(Ticket.objects.by_author(self.user_one)), 15)
        self.assertEqual(len(Ticket.objects.published()), 6)
        self.assertEqual(len(Ticket.objects.unpublished()), 13)

    def test_ticket_status(self):
        self.assertEqual(self.tickets_one[0].status, TICKET_STATUS.draft)
        self.assertEqual(self.tickets_two[0].status, TICKET_STATUS.published)
        self.assertEqual(self.tickets_three[0].status, TICKET_STATUS.draft)

    def test_ticket_tags(self):
        self.assertEqual(len(self.tickets_one[2].tags.similar_objects()), 5)
        self.assertEqual(len(self.tickets_two[2].tags.similar_objects()), 0)

    def tearDown(self):
        pass

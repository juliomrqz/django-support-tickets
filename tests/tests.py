#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-knowledgebase
------------

Tests for `django-knowledgebase` models module.
"""

from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from support_tickets.base.choices import TICKET_STATUS
from .mommy_recipes import user, category, ticket


class TicketCategorySetUpMixin(TestCase):

    def setUp(self):
        self.user_one = user.make()
        self.user_two = user.make()

        self.categories = category.make(author=self.user_one)
        self.categories_user_two = category.make(
            default_agent=self.user_two, _quantity=5
        )

        self.tickets_one = ticket.make(
            category=self.categories[0],
            submitter=self.user_one,

        )
        self.tickets_two = ticket.make(
            category=self.categories[1],
            submitter=self.user_one,
            status=TICKET_STATUS.open,

        )
        self.tickets_three = ticket.make(
            category=self.categories[2],
            submitter=self.user_one,
        )

        self.tickets_user_two = ticket.make(
            category=self.categories[0],
            submitter=self.user_two,
            _quantity=3
        )

        self.custom_ticket = ticket.make(
            title="Custom Ticket",
            category=self.categories[0],
            submitter=self.user_two,
            status=TICKET_STATUS.open,
            content="# Title",
            _quantity=1
        )

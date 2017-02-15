# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from support_tickets.apps import DjangoSupportTicketsConfig


class SettingsTestCase(TestCase):

    def setUp(self):
        self.AppConfig = DjangoSupportTicketsConfig

    def test_app_config(self):
        self.assertTrue(self.AppConfig.name, 'support_tickets')
        self.assertTrue(self.AppConfig.verbose_name, 'Support Tickets')

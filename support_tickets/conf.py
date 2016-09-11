# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections

from django.conf import settings as _settings
from django.core.signals import setting_changed
from django.dispatch import receiver


DEFAULTS = {
    'AUTO_ASSIGN_DEFAULT_AGENT': True,
    'ATTACHEMENTS_PATH': 'support/tickets/attachments',
    'MINIMUM_ATTACHEMENTS_PER_COMMENT': 0,
    'MAXIMUM_ATTACHEMENTS_PER_COMMENT': 3,
    'MAXIMUM_FILE_SIZE_PER_ATTACHEMENTS': 1024 * 1024 * 5,  # 5MB
}


class SupportTicketsSettings(collections.MutableMapping):
    """
    Container object for SupportTickets settings
    """

    def __init__(self, wrapped_settings):
        self.settings = DEFAULTS.copy()
        self.settings.update(wrapped_settings)

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, value):
        self.settings[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.settings)

    def __len__(self):
        return len(self.settings)

    def __getattr__(self, name):
        return self.__getitem__(name)


_settings_SUPPORT_TICKETS = []
if hasattr(_settings, "SUPPORT_TICKETS"):
    _settings_SUPPORT_TICKETS = _settings.SUPPORT_TICKETS

settings = SupportTicketsSettings(_settings_SUPPORT_TICKETS)


@receiver(setting_changed)
def reload_settings(**kwargs):
    if kwargs['setting'] == 'SUPPORT_TICKETS':
        settings.update(kwargs['value'])

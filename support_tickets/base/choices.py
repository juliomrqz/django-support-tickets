# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from model_utils import Choices

TICKET_STATUS = Choices(
    (0, 'open', _('Open')),
    (1, 'reopened', _('Reopened')),
    (2, 'resolved', _('Resolved')),
    (3, 'closed', _('Closed')),
    (4, 'duplicate', _('Duplicate')),
)

TICKET_PRIORITY = Choices(
    (1, 'critical', _('Critical')),
    (2, 'high', _('High')),
    (3, 'normal', _('Normal')),
    (4, 'low', _('Low')),
    (5, 'very_low', _('Very Low')),
)

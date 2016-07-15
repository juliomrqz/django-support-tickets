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
    (1, 'critical', _('1. Critical')),
    (2, 'high', _('2. High')),
    (3, 'normal', _('3. Normal')),
    (4, 'low', _('4. Low')),
    (5, 'very_low', _('5. Very Low')),
)

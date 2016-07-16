# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

from django_markup.fields import MarkupField
from model_utils.models import TimeStampedModel

from ..ticket.models import Ticket


class Comment(TimeStampedModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        verbose_name=_('User'),
        on_delete=models.CASCADE
    )

    ticket = models.ForeignKey(
        Ticket,
        related_name='comments',
        verbose_name=_('Ticket'),
    )

    description = models.TextField(
        _('Description'),
        help_text=_('Include as much detail as possible, including the steps to reproduce, error message(s), screen shots, URLs, date/time/duration, etc. This information will accelerate our ability to help you.'),
    )

    markup = MarkupField(default='none')

    class Meta:
        ordering = ['-created', ]
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

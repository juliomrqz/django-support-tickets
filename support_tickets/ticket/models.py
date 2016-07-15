# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

from django_markup.fields import MarkupField
from model_utils.models import TimeStampedModel

from ..base.choices import TICKET_STATUS, TICKET_PRIORITY
from ..conf import settings as tickets_settings
from ..models import Category


@python_2_unicode_compatible
class Ticket(TimeStampedModel):
    subject = models.CharField(
        _('Subject'),
        max_length=100,
        help_text=_('Type a brief summary of your question or issue.'),
    )

    category = models.ForeignKey(
        Category,
        verbose_name=_('Category'),
    )

    submitter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name='submitter',
        verbose_name=_('Submitter'),
        on_delete=models.CASCADE
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='tickets',
        blank=True,
        null=True,
        verbose_name=_('Agent'),
    )

    status = models.IntegerField(
        _('Status'),
        choices=TICKET_STATUS,
        default=TICKET_STATUS.open,
    )

    priority = models.IntegerField(
        _('Priority'),
        choices=TICKET_PRIORITY,
        default=TICKET_PRIORITY.normal,
        help_text=_('1 = Highest Priority, 5 = Low Priority'),
    )

    description = models.TextField(
        _('Description'),
        help_text=_('Include as much detail as possible, including the steps to reproduce, error message(s), screen shots, URLs, date/time/duration, etc. This information will accelerate our ability to help you.'),
    )

    markup = MarkupField(default='markdown')

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        if not self.priority:
            self.priority = self.TICKET_PRIORITY.normal

        if not self.agent and tickets_settings.AUTO_ASSIGN_DEFAULT_AGENT:
            default_agent = self.category.default_agent

            if default_agent:
                self.agent = default_agent

        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created', ]
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

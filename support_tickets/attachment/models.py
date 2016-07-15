# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeStampedModel

from ..comment.models import Comment


@python_2_unicode_compatible
class Attachment(TimeStampedModel):

    file = models.FileField(
        _('Attachment'),
        upload_to='support/tickets/attachments'
    )

    comment = models.ForeignKey(
        Comment,
        verbose_name=_('Comment'),
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='attachments',
        verbose_name=_('Uploader'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.file

    class Meta:
        ordering = ['-created', ]
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

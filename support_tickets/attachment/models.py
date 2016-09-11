# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import path

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible
from django.template.defaultfilters import truncatechars

from model_utils.models import TimeStampedModel

from ..comment.models import Comment
from ..base.utils import UploadTo


@python_2_unicode_compatible
class Attachment(TimeStampedModel):

    name = models.CharField(
        _('File name'),
        max_length=80,
        blank=True,
    )

    file = models.FileField(
        _('Attachment'),
        upload_to=UploadTo()
    )

    comment = models.ForeignKey(
        Comment,
        related_name='attachments',
        verbose_name=_('Comment'),
    )

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='attachments',
        verbose_name=_('Uploader'),
        on_delete=models.CASCADE
    )

    size = models.BigIntegerField(
        _('File Size'),
        blank=True,
        null=True,
        help_text=_('File size in bytes')
    )

    def save(self, *args, **kwargs):
        if self.file:
            self.size = self.file.size

        if not self.name:
            self.name = truncatechars(self.file.name, 80)

        super(Attachment, self).save(*args, **kwargs)

    @property
    def file_name(self):
        return path.basename(self.file.name)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created', ]
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

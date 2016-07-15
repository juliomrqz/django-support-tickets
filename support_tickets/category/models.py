# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeStampedModel
from treebeard.al_tree import AL_Node

from ..base.fields import CustomAutoSlugField


@python_2_unicode_compatible
class Category(AL_Node, TimeStampedModel):

    title = models.CharField(max_length=100)

    slug = CustomAutoSlugField()

    parent = models.ForeignKey(
        'self',
        related_name='children_set',
        null=True,
        db_index=True
    )

    order = models.IntegerField(default=0)

    default_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='default_agent',
        verbose_name=_('Default agent'),
        on_delete=models.CASCADE
    )

    active = models.BooleanField(default=True)

    node_order_by = ['order', 'title']

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', ]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

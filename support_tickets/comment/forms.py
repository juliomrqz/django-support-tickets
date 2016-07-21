# -*- coding: utf-8 -*-

from collections import OrderedDict

from django import forms

from betterforms.multiform import MultiModelForm

from ..attachment.forms import AttachmentForm

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('description',)


class CommentCreationForm(MultiModelForm):
    form_classes = OrderedDict((
        ('comment', CommentForm),
        ('attachments', AttachmentForm),
    ))

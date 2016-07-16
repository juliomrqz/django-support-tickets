# -*- coding: utf-8 -*-

from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext as _

from betterforms.multiform import MultiModelForm

from ..attachment.forms import AttachmentForm
from ..ticket.models import Ticket

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('description',)


class TicketStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketStatusForm, self).__init__(*args, **kwargs)

        self.fields['status'].label = _('New status')

    class Meta:
        model = Ticket
        fields = ('status',)


class CommentCreationForm(MultiModelForm):
    form_classes = OrderedDict((
        ('ticket', TicketStatusForm),
        ('comment', CommentForm),
        ('attachments', AttachmentForm),
    ))

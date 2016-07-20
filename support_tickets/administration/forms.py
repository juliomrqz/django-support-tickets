# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext as _

from betterforms.multiform import MultiModelForm

from ..attachment.forms import AttachmentForm
from ..comment.forms import CommentForm
from ..ticket.models import Ticket


class TicketPropertiesForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('status', 'category', 'priority', 'agent',)


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        self.fields['category'].empty_label = _('Select a category')

    class Meta:
        model = Ticket
        fields = ('subject', 'category', 'priority', 'submitter',)


class TicketStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketStatusForm, self).__init__(*args, **kwargs)

        self.fields['status'].empty_label = _('New status')

    class Meta:
        model = Ticket
        fields = ('status',)


class TicketCreationForm(MultiModelForm):
    form_classes = OrderedDict((
        ('ticket', TicketForm),
        ('comment', CommentForm),
        ('attachments', AttachmentForm),
    ))

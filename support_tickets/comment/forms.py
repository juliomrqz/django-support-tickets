# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('description',)

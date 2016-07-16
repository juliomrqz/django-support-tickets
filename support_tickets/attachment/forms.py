# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _
from django.template.defaultfilters import filesizeformat

from multiupload.fields import MultiFileField

from ..conf import settings as app_settings


class AttachmentForm(forms.Form):

    MINIMUM_ATTACHEMENTS = app_settings.MINIMUM_ATTACHEMENTS_PER_COMMENT
    MAXIMUM_ATTACHEMENTS = app_settings.MAXIMUM_ATTACHEMENTS_PER_COMMENT
    MAXIMUM_FILE_SIZE = app_settings.MAXIMUM_FILE_SIZE_PER_ATTACHEMENTS

    if MINIMUM_ATTACHEMENTS != 0:
        if MINIMUM_ATTACHEMENTS != MAXIMUM_ATTACHEMENTS:
            ATTACHMENTS_HELP_TEXT = _('Between %s and %s files') % (
                MINIMUM_ATTACHEMENTS, MAXIMUM_ATTACHEMENTS)

        else:
            ATTACHMENTS_HELP_TEXT = _('Maximum %s files') % MAXIMUM_ATTACHEMENTS

    else:
        ATTACHMENTS_HELP_TEXT = _('Maximum %s files') % MAXIMUM_ATTACHEMENTS

    ATTACHMENTS_HELP_TEXT += " " + _('(under <%s each)') % filesizeformat(MAXIMUM_FILE_SIZE)

    attachments = MultiFileField(
        min_num=MINIMUM_ATTACHEMENTS,
        max_num=MAXIMUM_ATTACHEMENTS,
        max_file_size=app_settings.MAXIMUM_FILE_SIZE_PER_ATTACHEMENTS,
        help_text=ATTACHMENTS_HELP_TEXT
    )

    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)

        self.fields['attachments'].required = self.MINIMUM_ATTACHEMENTS > 0

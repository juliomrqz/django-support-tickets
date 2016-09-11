# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import hashlib
import os
import uuid

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from ..conf import settings as app_settings


def send_email(request, subject, to, from_email, ctx, txt_template, html_template):

    # update ctx
    ctx.update({'website_domain': get_current_site(request).domain})

    # define text and HTML content
    text_content = get_template(txt_template).render(Context(ctx))
    html_content = get_template(html_template).render(Context(ctx))

    # Define email message objects
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


class UploadTo(object):
    ''' Based on: https://github.com/codingjoe/django-stdimage/blob/master/stdimage/utils.py '''
    file_pattern = "%(name)s%(ext)s"
    path_pattern = "%(path)s"

    def __call__(self, instance, filename):
        uploader = getattr(instance, 'uploader')
        uploader_id = hashlib.md5(str(uploader.pk)).hexdigest()[0:10]

        path, ext = os.path.splitext(filename)
        path, name = os.path.split(path)

        defaults = {
            'ext': ext,
            'name': name,
            'path': path,
            'class_name': instance.__class__.__name__,
        }

        defaults['path'] = app_settings.ATTACHEMENTS_PATH
        defaults.update(self.kwargs)

        return os.path.join(self.path_pattern % defaults,
                            uploader_id,
                            uuid.uuid4().hex,
                            self.file_pattern % defaults).lower()

    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args

    def deconstruct(self):
        path = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        return path, self.args, self.kwargs

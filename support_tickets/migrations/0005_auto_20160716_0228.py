# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_markup.fields


class Migration(migrations.Migration):

    dependencies = [
        ('support_tickets', '0004_auto_20160716_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='markup',
            field=django_markup.fields.MarkupField(default='none', max_length=255, verbose_name='markup', choices=[(b'none', b'None (no processing)'), (b'linebreaks', b'Linebreaks'), (b'markdown', b'Markdown'), (b'restructuredtext', 'reStructuredText')]),
        ),
    ]

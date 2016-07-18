# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_tickets', '0005_auto_20160716_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='size',
            field=models.BigIntegerField(help_text='File size in bytes', null=True, verbose_name='File Size', blank=True),
        ),
    ]

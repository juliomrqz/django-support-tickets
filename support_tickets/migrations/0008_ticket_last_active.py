# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('support_tickets', '0007_attachment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='last_active',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last active'),
        ),
    ]

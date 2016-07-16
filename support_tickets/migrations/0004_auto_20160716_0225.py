# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_tickets', '0003_auto_20160716_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.IntegerField(default=3, help_text='1 = Highest Priority, 5 = Lowest Priority', verbose_name='Priority', choices=[(1, 'Critical'), (2, 'High'), (3, 'Normal'), (4, 'Low'), (5, 'Very Low')]),
        ),
    ]

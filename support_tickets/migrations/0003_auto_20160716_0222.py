# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support_tickets', '0002_auto_20160715_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='comment',
            field=models.ForeignKey(related_name='attachments', verbose_name='Comment', to='support_tickets.Comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(related_name='comments', verbose_name='Ticket', to='support_tickets.Ticket'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.IntegerField(default=3, help_text='1 = Highest Priority, 5 = Low Priority', verbose_name='Priority', choices=[(1, 'Critical'), (2, 'High'), (3, 'Normal'), (4, 'Low'), (5, 'Very Low')]),
        ),
    ]

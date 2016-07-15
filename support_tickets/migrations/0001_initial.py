# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import support_tickets.base.fields
import model_utils.fields
import django_markup.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=100)),
                ('slug', support_tickets.base.fields.CustomAutoSlugField(editable=False, populate_from=b'title', unique=True, slugify=support_tickets.base.fields.custom_slugify)),
                ('default_agent', models.ForeignKey(related_name='default_agent', verbose_name='Default agent', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('subject', models.CharField(help_text='Type a brief summary of your question or issue.', max_length=100, verbose_name='Subject')),
                ('status', models.IntegerField(default=0, verbose_name='Status', choices=[(0, 'Open'), (1, 'Reopened'), (2, 'Resolved'), (3, 'Closed'), (4, 'Duplicate')])),
                ('priority', models.IntegerField(default=3, help_text='1 = Highest Priority, 5 = Low Priority', verbose_name='Priority', choices=[(1, '1. Critical'), (2, '2. High'), (3, '3. Normal'), (4, '4. Low'), (5, '5. Very Low')])),
                ('description', models.TextField(help_text='Include as much detail as possible, including the steps to reproduce, error message(s), screen shots, URLs, date/time/duration, etc. This information will accelerate our ability to help you.', verbose_name='Description')),
                ('markup', django_markup.fields.MarkupField(default='markdown', max_length=255, verbose_name='markup', choices=[(b'none', b'None (no processing)'), (b'linebreaks', b'Linebreaks'), (b'markdown', b'Markdown'), (b'restructuredtext', 'reStructuredText')])),
                ('agent', models.ForeignKey(related_name='tickets', verbose_name='Agent', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='support_tickets.Category')),
                ('submitter', models.ForeignKey(related_name='submitter', verbose_name='Submitter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_markup.fields
import model_utils.fields
import support_tickets.base.fields
import support_tickets.base.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(blank=True, max_length=80, verbose_name='File name')),
                ('file', models.FileField(upload_to=support_tickets.base.utils.UploadTo(), verbose_name='Attachment')),
                ('size', models.BigIntegerField(blank=True, help_text='File size in bytes', null=True, verbose_name='File Size')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=100)),
                ('slug', support_tickets.base.fields.CustomAutoSlugField(editable=False, populate_from=b'title', slugify=support_tickets.base.fields.custom_slugify, unique=True)),
                ('order', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('default_agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_agent', to=settings.AUTH_USER_MODEL, verbose_name='Default agent')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_set', to='support_tickets.Category')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.TextField(help_text='Include as much detail as possible, including the steps to reproduce, error message(s), screen shots, URLs, date/time/duration, etc. This information will accelerate our ability to help you.', verbose_name='Description')),
                ('markup', django_markup.fields.MarkupField(choices=[(b'none', b'None (no processing)'), (b'linebreaks', b'Linebreaks'), (b'markdown', b'Markdown'), (b'restructuredtext', 'reStructuredText')], default='none', max_length=255, verbose_name='markup')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('subject', models.CharField(help_text='Type a brief summary of your question or issue.', max_length=100, verbose_name='Subject')),
                ('status', models.IntegerField(choices=[(0, 'Open'), (1, 'Reopened'), (2, 'Resolved'), (3, 'Closed'), (4, 'Duplicate')], default=0, verbose_name='Status')),
                ('priority', models.IntegerField(choices=[(1, 'Critical'), (2, 'High'), (3, 'Normal'), (4, 'Low'), (5, 'Very Low')], default=3, help_text='1 = Highest Priority, 5 = Lowest Priority', verbose_name='Priority')),
                ('last_active', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last active')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to=settings.AUTH_USER_MODEL, verbose_name='Agent')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support_tickets.Category', verbose_name='Category')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitter', to=settings.AUTH_USER_MODEL, verbose_name='Submitter')),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='support_tickets.Ticket', verbose_name='Ticket'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='support_tickets.Comment', verbose_name='Comment'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to=settings.AUTH_USER_MODEL, verbose_name='Uploader'),
        ),
    ]

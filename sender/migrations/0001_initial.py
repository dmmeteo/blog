# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_from', models.CharField(default=b'SimpleBlog', max_length=11)),
                ('number_to', models.CharField(max_length=14)),
                ('message', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('dlr_timestamp', models.DateTimeField()),
                ('priority', models.CharField(blank=True, max_length=1, choices=[(b'', b'-----'), (b'1', b'Low'), (b'2', b'Normal'), (b'3', b'High')])),
                ('system_type', models.CharField(max_length=8, blank=True)),
                ('status', models.CharField(max_length=12, blank=True)),
                ('parts', models.CharField(max_length=1, blank=True)),
                ('cost', models.CharField(max_length=10, blank=True)),
                ('message_id', models.CharField(max_length=256, blank=True)),
                ('country', models.CharField(max_length=2, null=True, blank=True)),
                ('mccmnc', models.CharField(max_length=6, blank=True)),
                ('username', models.ForeignKey(default=b'1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

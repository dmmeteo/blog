# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0002_remove_smsmessage_dlr_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsmessage',
            name='dlr_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.CharField(max_length=80, null=True, verbose_name='Event id', blank=True),
        ),
    ]

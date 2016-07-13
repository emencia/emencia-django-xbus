# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbus', '0002_event_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='xref',
            field=models.CharField(max_length=80, verbose_name='External Ref'),
        ),
    ]

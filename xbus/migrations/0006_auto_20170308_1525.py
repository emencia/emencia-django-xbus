# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-08 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbus', '0005_auto_20170110_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='direction',
            field=models.CharField(choices=[(b'in', 'Incoming'), (b'out', 'Outgoing'), (b'immediate-out', 'Immediate-Out')], max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='state',
            field=models.CharField(choices=[(b'draft', 'Draft'), (b'pending', 'Pending'), (b'done', 'Done'), (b'error', 'Error')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='envelope',
            name='state',
            field=models.CharField(choices=[(b'draft', 'Draft'), (b'pending', 'Pending'), (b'done', 'Done'), (b'error', 'Error')], max_length=20),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xbus', '0003_auto_20160713_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Comment'),
        ),
    ]

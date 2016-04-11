# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True)),
                ('xref', models.CharField(max_length=36, verbose_name='External Ref')),
                ('xbus_message_correlation_id', models.CharField(max_length=36, verbose_name='Message correlation id')),
                ('event_type', models.CharField(max_length=80, verbose_name='Event type')),
                ('direction', models.CharField(max_length=25, verbose_name='Direction', choices=[(b'in', 'Incoming'), (b'out', 'Outgoing'), (b'immediate-out', 'Immediate-Out')])),
                ('state', models.CharField(max_length=20, verbose_name='State', choices=[(b'pending', 'Pending'), (b'done', 'Done'), (b'error', 'Error')])),
                ('comment', models.TextField(verbose_name='Commentaire', blank=True)),
                ('item', models.BinaryField(verbose_name='Event item')),
                ('admin_url', models.CharField(default=b'', max_length=250, null=True, editable=False)),
            ],
        ),
    ]

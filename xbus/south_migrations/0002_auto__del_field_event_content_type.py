# -*- coding: utf-8 -*-
# flake8: noqa
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.content_type'
        db.delete_column(u'xbus_event', 'content_type_id')


    def backwards(self, orm):
        # Adding field 'Event.content_type'
        db.add_column(u'xbus_event', 'content_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['contenttypes.ContentType']),
                      keep_default=False)


    models = {
        u'xbus.event': {
            'Meta': {'object_name': 'Event'},
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.BinaryField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'xbus_message_correlation_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'xref': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        }
    }

    complete_apps = ['xbus']

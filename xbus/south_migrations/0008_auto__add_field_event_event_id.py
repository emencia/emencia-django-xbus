# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.event_id'
        db.add_column(u'xbus_event', 'event_id',
                      self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Event.event_id'
        db.delete_column(u'xbus_event', 'event_id')


    models = {
        u'xbus.event': {
            'Meta': {'object_name': 'Event'},
            'admin_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'event_id': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.BinaryField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'xbus_message_correlation_id': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'xref': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        }
    }

    complete_apps = ['xbus']
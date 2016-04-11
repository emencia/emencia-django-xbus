# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'xbus_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('xref', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('xbus_message_correlation_id', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('direction', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('item', self.gf('django.db.models.fields.BinaryField')()),
        ))
        db.send_create_signal(u'xbus', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'xbus_event')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'xbus.event': {
            'Meta': {'object_name': 'Event'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
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
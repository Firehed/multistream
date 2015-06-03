# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Channel.channel_id'
        db.delete_column(u'main_channel', 'channel_id')

        # Adding field 'Channel.name'
        db.add_column(u'main_channel', 'name',
                      self.gf('django.db.models.fields.CharField')(default='new', max_length=60),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Channel.channel_id'
        db.add_column(u'main_channel', 'channel_id',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=60),
                      keep_default=False)

        # Deleting field 'Channel.name'
        db.delete_column(u'main_channel', 'name')


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channel_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'stream_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['main']
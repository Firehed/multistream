# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Channel.is_live'
        db.delete_column(u'main_channel', 'is_live')

        # Adding field 'Channel.live'
        db.add_column(u'main_channel', 'live',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Channel.is_live'
        db.add_column(u'main_channel', 'is_live',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Channel.live'
        db.delete_column(u'main_channel', 'live')


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channel_id': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'channel_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'stream_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['main']
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Channel.live'
        db.delete_column(u'main_channel', 'live')

        # Deleting field 'Channel.last_checked'
        db.delete_column(u'main_channel', 'last_checked')


    def backwards(self, orm):
        # Adding field 'Channel.live'
        db.add_column(u'main_channel', 'live',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Channel.last_checked'
        db.add_column(u'main_channel', 'last_checked',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channel_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'stream_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['main']
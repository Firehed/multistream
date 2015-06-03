# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Channel.channel_obj'
        db.delete_column(u'main_channel', 'channel_obj')

        # Deleting field 'Channel.stream_obj'
        db.delete_column(u'main_channel', 'stream_obj')

        # Adding field 'Channel.logo'
        db.add_column(u'main_channel', 'logo',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Channel.preview'
        db.add_column(u'main_channel', 'preview',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Channel.game'
        db.add_column(u'main_channel', 'game',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=60, blank=True),
                      keep_default=False)

        # Adding field 'Channel.live'
        db.add_column(u'main_channel', 'live',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Channel.channel_obj'
        db.add_column(u'main_channel', 'channel_obj',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Channel.stream_obj'
        db.add_column(u'main_channel', 'stream_obj',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Channel.logo'
        db.delete_column(u'main_channel', 'logo')

        # Deleting field 'Channel.preview'
        db.delete_column(u'main_channel', 'preview')

        # Deleting field 'Channel.game'
        db.delete_column(u'main_channel', 'game')

        # Deleting field 'Channel.live'
        db.delete_column(u'main_channel', 'live')


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'preview': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Tag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['main']
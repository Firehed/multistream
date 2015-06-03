# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Tag.firstDate'
        db.add_column(u'main_tag', 'firstDate',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Tag.lastDate'
        db.add_column(u'main_tag', 'lastDate',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Tag.firstDate'
        db.delete_column(u'main_tag', 'firstDate')

        # Deleting field 'Tag.lastDate'
        db.delete_column(u'main_tag', 'lastDate')


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'game': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'preview': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Tag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'firstDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'lastDate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['main']
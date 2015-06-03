# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'main_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'main', ['Tag'])

        # Adding M2M table for field tags on 'Channel'
        db.create_table(u'main_channel_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm[u'main.channel'], null=False)),
            ('tag', models.ForeignKey(orm[u'main.tag'], null=False))
        ))
        db.create_unique(u'main_channel_tags', ['channel_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'main_tag')

        # Removing M2M table for field tags on 'Channel'
        db.delete_table('main_channel_tags')


    models = {
        u'main.channel': {
            'Meta': {'object_name': 'Channel'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'channel_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'stream_obj': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Tag']", 'symmetrical': 'False'})
        },
        u'main.tag': {
            'Meta': {'object_name': 'Tag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['main']
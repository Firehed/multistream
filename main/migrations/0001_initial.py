# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('active', models.BooleanField(default=False)),
                ('logo', models.URLField(blank=True)),
                ('preview', models.URLField(blank=True)),
                ('game', models.CharField(max_length=60, blank=True)),
                ('live', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('active', models.BooleanField(default=False)),
                ('index', models.IntegerField(null=True)),
                ('firstDate', models.DateField(null=True)),
                ('lastDate', models.DateField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='channel',
            name='tags',
            field=models.ManyToManyField(related_name='channels', to='main.Tag', blank=True),
            preserve_default=True,
        ),
    ]

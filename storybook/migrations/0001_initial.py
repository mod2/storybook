# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('json', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(null=True, blank=True)),
                ('status', models.CharField(max_length=10, choices=[('active', 'Active'), ('complete', 'Complete'), ('deleted', 'Deleted')])),
                ('synopsis', models.TextField(null=True, blank=True)),
                ('order', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(default=datetime.datetime(2015, 2, 16, 20, 35, 16, 907775, tzinfo=utc), auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('status', models.CharField(max_length=10, choices=[('active', 'Active'), ('finished', 'Finished'), ('inactive', 'Inactive')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(default=datetime.datetime(2015, 2, 16, 20, 35, 16, 906988, tzinfo=utc), auto_now=True)),
                ('order', models.PositiveSmallIntegerField(default=50000)),
                ('word_count', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scene',
            name='story',
            field=models.ForeignKey(related_name='scenes', to='storybook.Story'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revision',
            name='scene',
            field=models.ForeignKey(related_name='revisions', to='storybook.Scene'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historyentry',
            name='story',
            field=models.ForeignKey(related_name='history_entries', to='storybook.Story'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 18:00
from __future__ import unicode_literals

import autoslug.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0004_auto_20150520_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scene',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 18, 0, 4, 856021, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='scene',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 18, 0, 4, 856055, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='story',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 18, 0, 4, 854975, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='story',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 9, 18, 0, 4, 855246, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title'),
        ),
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('abandoned', 'Abandoned'), ('finished', 'Finished')], default='active', max_length=10),
        ),
    ]
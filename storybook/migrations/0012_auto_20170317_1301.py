# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0011_auto_20170317_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='character',
            name='scenes',
        ),
        migrations.RemoveField(
            model_name='character',
            name='story',
        ),
        migrations.RemoveField(
            model_name='revision',
            name='scene',
        ),
        migrations.RenameField(
            model_name='draft',
            old_name='json',
            new_name='story_text',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='status',
        ),
        migrations.RemoveField(
            model_name='scene',
            name='synopsis',
        ),
        migrations.RemoveField(
            model_name='story',
            name='description',
        ),
        migrations.AddField(
            model_name='scene',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Character',
        ),
        migrations.DeleteModel(
            name='Revision',
        ),
    ]

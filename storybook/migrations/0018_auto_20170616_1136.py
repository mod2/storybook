# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-16 17:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0017_scene_word_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fragment',
            name='story',
        ),
        migrations.DeleteModel(
            name='Fragment',
        ),
    ]

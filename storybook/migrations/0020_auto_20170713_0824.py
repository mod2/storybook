# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-13 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0019_inbox_inboxentry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inbox',
            options={'verbose_name_plural': 'inboxes'},
        ),
        migrations.AlterModelOptions(
            name='inboxentry',
            options={'ordering': ['created'], 'verbose_name_plural': 'inbox entries'},
        ),
        migrations.AddField(
            model_name='inbox',
            name='html',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historyentry',
            options={'verbose_name_plural': 'history entries'},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name_plural': 'stories'},
        ),
        migrations.AddField(
            model_name='story',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='tanglewood', editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scene',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 16, 20, 45, 9, 796043, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scene',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scene',
            name='status',
            field=models.CharField(default='active', max_length=10, choices=[('active', 'Active'), ('complete', 'Complete'), ('deleted', 'Deleted')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 16, 20, 45, 9, 795224, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='order',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
    ]

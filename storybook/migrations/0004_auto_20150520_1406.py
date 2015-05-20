# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0003_auto_20150217_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 20, 6, 57, 967302, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 20, 20, 6, 57, 966580, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='order',
            field=models.PositiveSmallIntegerField(default=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(default='active', max_length=10, choices=[('active', 'Active'), ('finished', 'Finished'), ('inactive', 'Inactive')]),
            preserve_default=True,
        ),
    ]

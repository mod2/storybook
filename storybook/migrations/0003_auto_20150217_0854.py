# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0002_auto_20150216_1345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='revision',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='story',
            name='word_count',
        ),
        migrations.AlterField(
            model_name='scene',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 17, 15, 54, 41, 846370, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='story',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 17, 15, 54, 41, 845522, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]

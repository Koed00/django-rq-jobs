# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.CharField(max_length=100, choices=[(b'clean_sessions', b'Clean Sessions')])),
                ('args', models.CharField(max_length=255, null=True, blank=True)),
                ('schedule_type', models.CharField(default=b'O', max_length=1, verbose_name='Schedule Type', choices=[(b'O', 'Once'), (b'H', 'Hourly'), (b'D', 'Daily'), (b'W', 'Weekly'), (b'M', 'Monthly'), (b'Q', 'Quarterly'), (b'Y', 'Yearly')])),
                ('repeats', models.SmallIntegerField(default=-1, verbose_name='Repeats')),
                ('next_run', models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Next Run')),
                ('last_run', models.DateTimeField(verbose_name='Last Run', null=True, editable=False)),
                ('rq_id', models.CharField(max_length=64, null=True, editable=False)),
                ('rq_origin', models.CharField(max_length=64, null=True, editable=False)),
            ],
            options={
                'ordering': ['next_run'],
                'verbose_name_plural': 'Scheduled jobs',
            },
        ),
    ]

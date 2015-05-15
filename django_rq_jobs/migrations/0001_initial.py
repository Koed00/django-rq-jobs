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
                ('task', models.CharField(choices=[], max_length=100)),
                ('args', models.CharField(blank=True, max_length=255, null=True)),
                ('schedule_type', models.CharField(choices=[('O', 'Once'), ('H', 'Hourly'), ('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly'), ('Q', 'Quarterly'), ('Y', 'Yearly')], verbose_name='Schedule Type', max_length=1, default='O')),
                ('repeats', models.SmallIntegerField(verbose_name='Repeats', default=-1)),
                ('next_run', models.DateTimeField(verbose_name='Next Run', null=True, default=django.utils.timezone.now)),
                ('last_run', models.DateTimeField(verbose_name='Last Run', null=True, editable=False)),
                ('rq_id', models.CharField(editable=False, max_length=64, null=True)),
                ('rq_origin', models.CharField(editable=False, max_length=64, null=True)),
            ],
            options={
                'verbose_name_plural': 'Scheduled jobs',
                'ordering': ['next_run'],
            },
        ),
    ]

# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Job


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'task',
        'schedule_type',
        'repeats',
        'last_run',
        'next_run',
        'rq_link',
        'rq_status'
    )
    list_filter = ('last_run', 'next_run', 'schedule_type')
admin.site.register(Job, ScheduleAdmin)


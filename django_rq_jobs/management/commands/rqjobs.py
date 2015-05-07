from ast import literal_eval
import importlib

import arrow
from django.conf import settings
from django.core.management.base import BaseCommand
import django_rq
from django_rq_jobs.models import Job


class Command(BaseCommand):
    help = "Queues scheduled jobs"

    def handle(self, *args, **options):
        for job in Job.objects.exclude(repeats=0).filter(next_run__lt=arrow.utcnow().datetime):
            task = getattr(importlib.import_module(settings.RQ_JOBS_MODULE), job.task)
            try:
                if job.args:
                    rq = django_rq.enqueue(task, **literal_eval(job.args))
                else:
                    rq = django_rq.enqueue(task)
                job.rq_id = rq.id
                job.rq_origin = rq.origin
            except NameError:
                self.stdout.write('Error: Unknown task')
                continue
            job.last_run = arrow.utcnow().datetime
            self.stdout.write('{} queued'.format(job.get_task_display()))
            if job.schedule_type != Job.ONCE:
                if job.repeats < 0 or job.repeats > 1:
                    next_run = arrow.get(job.next_run)
                    if job.schedule_type == Job.HOURLY:
                        next_run = next_run.replace(hours=+1)
                    elif job.schedule_type == Job.DAILY:
                        next_run = next_run.replace(days=+1)
                    elif job.schedule_type == Job.WEEKLY:
                        next_run = next_run.replace(weeks=+1)
                    elif job.schedule_type == Job.MONTHLY:
                        next_run = next_run.replace(months=+1)
                    elif job.schedule_type == Job.QUARTERLY:
                        next_run = next_run.replace(months=+3)
                    elif job.schedule_type == Job.YEARLY:
                        next_run = next_run.replace(years=+1)
                    job.next_run = next_run.datetime
                    if job.repeats > 1:
                        job.repeats += -1
                    self.stdout.write('Next run {}'.format(next_run.humanize()))
                    job.save()
                else:
                    job.delete()
                    self.stdout.write('Deleting limited run task')
            else:
                self.stdout.write('Deleting run once task')
                job.delete()
        self.stdout.write('Done')
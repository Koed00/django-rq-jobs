from ast import literal_eval

import arrow
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
import django_rq

from django_rq_jobs.models import Job


class Command(BaseCommand):
    help = _("Queues scheduled jobs")
    BaseCommand.can_import_settings = True
    BaseCommand.requires_system_checks = True
    BaseCommand.leave_locale_alone = True

    def handle(self, *args, **options):
        for job in Job.objects.exclude(repeats=0).filter(next_run__lt=arrow.utcnow().datetime):
            if job.args:
                rq = django_rq.enqueue(job.rq_task, **literal_eval(job.args))
            else:
                rq = django_rq.enqueue(job.rq_task)
            job.rq_id = rq.id
            job.rq_origin = rq.origin
            job.last_run = arrow.utcnow().datetime
            self.stdout.write(_('* Queueing {} on {}.').format(job.get_task_display(), job.rq_origin), ending=' ')
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
                    self.stdout.write(_('Next run {}.').format(next_run.humanize()))
                    job.save()
                else:
                    job.delete()
                    self.stdout.write(_('Deleting limited run task'))
            else:
                self.stdout.write(_('Deleting run once task'))
                job.delete()
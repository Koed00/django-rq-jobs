import importlib
from types import FunctionType

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_rq import get_connection
from django_rq.settings import QUEUES_LIST
from rq.exceptions import NoSuchJobError
from rq.job import Job as RQJob


def underscore_to_camelcase(word):
    """
    Humanizes function names
    """
    return ' '.join(char.capitalize() for char in word.split('_'))


def queue_index_by_name(name):
    """
    Reverse lookups the queue index used by django_rq
    Need this for links to the django_rq admin pages
    """
    for index, config in enumerate(QUEUES_LIST):
        if config['name'] == name:
            return index
    return 0


def task_list():
    """
    Scans the module set in RQ_JOBS_MODULE for RQ jobs decorated with @task
    Compiles a readable list for Job model task choices
    """
    choices = []
    try:
        tasks = importlib.import_module(settings.RQ_JOBS_MODULE)
        t = [x for x, y in tasks.__dict__.items() if type(y) == FunctionType and hasattr(y, 'delay')]
        for j in t:
            choices.append((j, underscore_to_camelcase(j)))
        choices.sort(key=lambda tup: tup[1])
    except AttributeError:
        raise ImproperlyConfigured(_("You have to define RQ_JOBS_MODULE in settings.py"))
    except ImportError:
        raise ImproperlyConfigured(_("Can not find module {}").format(settings.RQ_JOBS_MODULE))
    return choices


class Job(models.Model):
    task = models.CharField(max_length=100, choices=task_list())
    args = models.CharField(max_length=255, null=True, blank=True)
    ONCE = 'O'
    HOURLY = 'H'
    DAILY = 'D'
    WEEKLY = 'W'
    MONTHLY = 'M'
    QUARTERLY = 'Q'
    YEARLY = 'Y'
    TYPE = (
        (ONCE, _('Once')),
        (HOURLY, _('Hourly')),
        (DAILY, _('Daily')),
        (WEEKLY, _('Weekly')),
        (MONTHLY, _('Monthly')),
        (QUARTERLY, _('Quarterly')),
        (YEARLY, _('Yearly')),
    )
    schedule_type = models.CharField(max_length=1, choices=TYPE, default=TYPE[0][0], verbose_name=_('Schedule Type'))
    repeats = models.SmallIntegerField(default=-1, verbose_name=_('Repeats'))
    next_run = models.DateTimeField(verbose_name=_('Next Run'), default=timezone.now, null=True)
    last_run = models.DateTimeField(verbose_name=_('Last Run'), editable=False, null=True)
    rq_id = models.CharField(max_length=64, editable=False, null=True)
    rq_origin = models.CharField(max_length=64, editable=False, null=True)

    @property
    def rq_job(self):
        if not self.rq_id or not self.rq_origin:
            return
        try:
            return RQJob.fetch(self.rq_id, connection=get_connection(self.rq_origin))
        except NoSuchJobError:
            return

    def rq_status(self):
        if self.rq_job:
            return self.rq_job.status

    def rq_link(self):
        if self.rq_job:
            url = reverse('rq_job_detail',
                          kwargs={'job_id': self.rq_id, 'queue_index': queue_index_by_name(self.rq_origin)})
            return '<a href="{}">{}</a>'.format(url, self.rq_id)

    @property
    def rq_task(self):
        tasks = importlib.import_module(settings.RQ_JOBS_MODULE)
        return getattr(tasks, self.task)

    rq_link.allow_tags = True

    class Meta:
        ordering = ['next_run']
        verbose_name_plural = _("Scheduled jobs")

    def __unicode__(self):
        return self.get_task_display()

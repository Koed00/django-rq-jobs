from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured

from django.test import TestCase, override_settings
from django.utils import timezone

from django.utils.translation import activate
from django.core import management
from django_rq import get_failed_queue

from django_rq_jobs.models import underscore_to_camelcase, task_list, queue_index_by_name, Job


class RQJobsTestCase(TestCase):
    @override_settings(RQ_JOBS_MODULE='django_rq_jobs.tests.tasks')
    def setUp(self):
        activate('en-en')
        Job.objects.create(task='django_check', schedule_type=Job.HOURLY)
        Job.objects.create(task='django_check', schedule_type=Job.WEEKLY)
        Job.objects.create(task='django_check', schedule_type=Job.MONTHLY)
        Job.objects.create(task='django_check', schedule_type=Job.QUARTERLY)
        Job.objects.create(task='django_check', schedule_type=Job.YEARLY)
        Job.objects.create(task='django_arg_check', schedule_type=Job.ONCE, args={'verbosity': 3})

    def test_camel_case(self):
        self.assertEqual(underscore_to_camelcase('this_is_a_function'), 'This Is A Function')

    @override_settings(RQ_JOBS_MODULE='django_rq_jobs.tests.tasks')
    def test_task_list(self):
        self.assertEqual(task_list(), [('django_arg_check', 'Django Arg Check'), ('django_check', 'Django Check')])
        with self.settings(RQ_JOBS_MODULE=None):
            self.assertRaises(ImproperlyConfigured, task_list)


    @override_settings(RQ_QUEUES="{'high': {},'default': {}, 'low': {}")
    def test_queue_index_by_name(self):
        self.assertEqual(queue_index_by_name('default'), 1)
        self.assertEqual(queue_index_by_name('nomnom'), 0)

    @override_settings(RQ_JOBS_MODULE='django_rq_jobs.tests.tasks')
    def test_create_job(self):
        """test simple job creation """
        test_job = Job.objects.get(task='django_check', schedule_type=Job.HOURLY)
        self.assertEqual(test_job.task, 'django_check')
        self.assertEqual(test_job.args, None)
        self.assertEqual(test_job.schedule_type, Job.HOURLY)
        self.assertEqual(test_job.repeats, -1)
        self.assertEqual(test_job.last_run, None)
        self.assertTrue(test_job.next_run < timezone.now())
        self.assertEqual(test_job.rq_id, None)
        self.assertEqual(test_job.rq_job, None)
        self.assertEqual(test_job.rq_link(), None)
        self.assertEqual(test_job.rq_origin, None)
        self.assertEqual(test_job.rq_status(), None)

    @override_settings(RQ_JOBS_MODULE='django_rq_jobs.tests.tasks')
    def test_run_job(self):
        """run a job and check if it's rescheduled properly"""
        management.call_command('rqjobs')
        test_job = Job.objects.get(task='django_check', schedule_type=Job.HOURLY)
        self.assertNotEqual(test_job.rq_id, None)
        self.assertNotEqual(test_job.rq_origin, None)
        self.assertNotEqual(test_job.rq_job, None)
        self.assertNotEqual(test_job.rq_status(), None)
        self.assertNotEqual(test_job.rq_origin, None)
        self.assertNotEqual(test_job.rq_link(), None)
        self.assertNotEqual(test_job.last_run, None)
        self.assertTrue(test_job.next_run > timezone.now())

    @override_settings(RQ_JOBS_MODULE='django_rq_jobs.tests.tasks')
    def test_run_once_job(self):
        """run an single run job with arguments and check if it gets deleted"""
        test_job = Job.objects.get(task='django_arg_check')
        management.call_command('rqjobs')
        self.assertFalse(Job.objects.filter(pk=test_job.pk).exists())

    @override_settings(RQ_JOBS_MODULE='django_rq_jobs.tests.tasks')
    def test_run_limited_job(self):
        """run a limited run job twice to see if it counts down and gets deleted"""
        test_job = Job.objects.create(task='django_check', schedule_type=Job.HOURLY, repeats=2,
                                      next_run=timezone.now() + timedelta(hours=-2))
        management.call_command('rqjobs')
        self.assertEqual(Job.objects.get(pk=test_job.pk).repeats, 1)
        management.call_command('rqjobs')
        self.assertFalse(Job.objects.filter(pk=test_job.pk).exists())

    def tearDown(self):
        q = get_failed_queue()
        q.empty()


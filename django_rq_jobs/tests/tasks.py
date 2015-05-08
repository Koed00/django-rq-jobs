from django_rq import job
from django.core import management


@job
def django_check():
    return management.call_command('check')


@job
def django_arg_check(verbosity):
    if not verbosity:
        raise ValueError
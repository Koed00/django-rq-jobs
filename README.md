=====
Django RQ Jobs
=====

Provides scheduled jobs management from the Django Admin using [Django-RQ](https://github.com/ui/django-rq)

Requirements
------------

* [Django](https://www.djangoproject.com)
* [Django-RQ](https://github.com/ui/django-rq)
* [Arrow](https://github.com/crsmithdev/arrow)

Installation
-----------

* Make sure you have [Django-RQ](https://github.com/ui/django-rq) up and running before you do anything.
   This app is just a simple admin plugin to manage your scheduled tasks and management commands.

* Install the package with  `pip install django-rq-jobs`  

* Add `django_rq_jobs` to INSTALLED_APPS in settings.py:
```
INSTALLED_APPS = (
    # other apps
    "django_rq",
    "django_rq_jobs",
)
```
* Add `RQ_JOBS_MODULE` in settings.py:
```
RQ_JOBS_MODULE = 'myapp.tasks'
```
This will point RQ Jobs to where you keep your jobs. Anything marked with the  Django RQ's `@job` decorator 
will show up in the admin.

* Run `python manage.py migrate` to create the job model.

* Open your Django admin and find the RQ Jobs scheduled job section and schedule something.

* Schedule the heartbeat `python manage.py rqjobs` with your favorite scheduler.
    This can be cron, Heroku scheduler or anything else you prefer.
    Make sure you set the heartbeat interval to something sensible;
    5 or 10 minutes is usually enough, but run it every minute if you want.
    Execution of the jobs is deferred to RQ anyway.
    
Notes
-----
* Supports hourly, daily, weekly, monthly, quarterly and yearly scheduled tasks.
* Limited run schedules: Set the 'Repeats' on a task to the maxium number of repeats you want. The task gets deleted once the counter reaches zero.
*RQ Jobs will try to link a job to a queue task status in RQ. Usually these job reports don't exist much longer than a few minutes unless they fail. So if you are seeing `None` in the RQ status, that usually means things went well.
*If you haven't run the heartbeat `manage.py rqjobs` for a while and missed some scheduled jobs, RQ Jobs will play catch-up with every heartbeat.
 So if you missed an hourly tasks 12 times and restart with a 5 minute heartbeat, your task will run every 5 minutes until it catches up with the current schedule.
 This way limited run schedules don't get compromised.
 
Management Commmands
--------------------
If you want to schedule regular Django management commands, the best way is to add them is using Django's management wrapper.
So if you wanted to schedule `manage.py clearsessions' :

```
from django import management


@job
def clear_sessions():
    return management.call_command('clearsessions')

```

This will automagically appear as 'Clear Sessions' in the admin interface.


Todo
-----
* Create tests
* Test with older versions of Django and maybe lower the 1.7 requirement
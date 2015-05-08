from setuptools import setup


setup(
    name='django-rq-jobs',
    version='0.1.3',
    author='Ilan Steemers',
    author_email='koed00@gmail.com',
    packages=['django_rq_jobs'],
    url='https://github.com/koed00/django-rq-jobs',
    license='MIT',
    description='Provides scheduled jobs from the Django Admin using Django-RQ',
    long_description='Run cron-like jobs on distributed queues from your django admin using Django-RQ. '
                     'Supports Once, Hourly, Weekly, Monthly, Quarterly and Yearly schedules.'
                     'Requires Django, Django-RQ and Arrow',
    include_package_data=True,
    install_requires=['django>=1.7', 'django-rq>=0.8.0', 'arrow>=0.5.4'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
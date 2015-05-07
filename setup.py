import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-rq-jobs',
    version='0.1.0',
    author='Ilan Steemers',
    author_email='koed00@gmail.com',
    packages=['django_rq_jobs'],
    url='https://github.com/ui/django-rq-jobs',
    license='MIT',
    description='Provides scheduled jobs from the Django Admin using django-rq',
    long_description=README,
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
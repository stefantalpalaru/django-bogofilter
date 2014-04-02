#!/usr/bin/env python

"""
Adapted from django-contrib-comments, which itself was adapted from django-constance, which itself was adapted from django-adminfiles.
"""

import os
import sys

here = os.environ['PWD'] # make it work with symlinks
if not here.endswith('/tests'):
    here += '/tests'
parent = os.path.dirname(here)
sys.path[0:0] = [here, parent]

from django.conf import settings
settings.configure(
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}},
    INSTALLED_APPS = [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.sites",
        "django.contrib.admin",
        "django_comments",
        "bogofilter",
        "testapp",
        "custom_comments",
    ],
    ROOT_URLCONF = 'testapp.urls',
    SECRET_KEY = "it's a secret to everyone",
    SITE_ID = 1,
    COMMENTS_APP = 'bogofilter',
    BOGOFILTER_ARGS = ['-d', './bogofilter_test_dir'],
)

from django.test.simple import DjangoTestSuiteRunner

def main():
    runner = DjangoTestSuiteRunner(failfast=False, verbosity=1)
    failures = runner.run_tests(['testapp'], interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()

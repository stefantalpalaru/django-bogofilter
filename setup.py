#!/usr/bin/env python

from setuptools import setup

setup(name='django-bogofilter',
      version='0.2',
      description='Bayesian spam filtering for django_comments using bogofilter',
      long_description=open("README.rst").read(),
      author='Stefan Talpalaru',
      author_email='stefantalpalaru@yahoo.com',
      url='https://github.com/stefantalpalaru/django-bogofilter',
      license = 'BSD',
      packages=['bogofilter'],
      test_suite='tests.runtests.main',
      install_requires=['Django', 'django-contrib-comments'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: POSIX',
      ],
     )


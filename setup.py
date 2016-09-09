#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import support_tickets

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = support_tickets.__version__

if sys.argv[-1] == 'publish':
    try:
        import wheel
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='django-support-tickets',
    version=version,
    description="""A support tickets system made with Django""",
    long_description=readme + '\n\n' + history,
    author='Julio Marquez',
    author_email='j@bazzite.com',
    url='https://github.com/bazzite/django-support-tickets',
    packages=[
        'support_tickets',
    ],
    include_package_data=True,
    install_requires=install_requires,
    license="Apache",
    zip_safe=False,
    keywords='django-support-tickets',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

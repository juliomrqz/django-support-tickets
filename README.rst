=============================
Django Support Tickets
=============================

.. image:: https://badge.fury.io/py/django-support-tickets.svg
    :target: https://badge.fury.io/py/django-support-tickets

.. image:: https://travis-ci.org/bazzite/django-support-tickets.svg?branch=master
    :target: https://travis-ci.org/bazzite/django-support-tickets

.. image:: https://codecov.io/gh/bazzite/django-support-tickets/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bazzite/django-support-tickets

Another Support Tickets Django App

Documentation
-------------

The full documentation is at https://django-support-tickets.bazzite.com.

Quickstart
----------

Install Django Support Tickets::

    pip install django-support-tickets

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'support_tickets.apps.SupportTicketsConfig',
        ...
    )

Add Django Support Tickets's URL patterns:

.. code-block:: python

    from support_tickets import urls as support_tickets_urls


    urlpatterns = [
        ...
        url(r'^', include(support_tickets_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

=====
Usage
=====

To use Django Support Tickets in a project, add it to your `INSTALLED_APPS`:

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

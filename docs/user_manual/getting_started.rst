===============
Getting started
===============


Installation and configuration
==============================

The package and its dependencies can be installed from PyPI via ``pip install -U django-gsheets-import``.
To use the package in your Django project, just add ``import_export`` and ``gsheets_import`` to the list of **installed apps** in your ``settings.py``, i.e.

.. code-block:: python

    ## in settings.py
    INSTALLED_APPS = [
        ...,
        'import_export',
        'gsheets_import',
        ...
    ]

In order for ``django-gsheets-import`` to work properly, it needs to be associated with an underlying **Google Cloud Project** (GCP).
How to properly set up an appropriate GCP using the Google Cloud Console is described in more detail in the corresponding :doc:`section <google_cloud_project>`.
At this point, let us just note that all of the services needed are available in Google Cloud's `Free Tier <https://cloud.google.com/free/>`_, so that there is no need to set up a billing account.
Assuming that a suitable GCP already exists, go to the `Google Cloud Console <https://console.cloud.google.com/>`_ and navigate to ``APIs & Services > Credentials``.
From there, copy the **project number**, an **API key**, as well as the desired **OAuth Client ID** and add them to your ``settings.py``, i.e.

.. code-block:: python

    ## in settings.py
    GSHEETS_IMPORT_APP_ID = '<Your project number>'
    GSHEETS_IMPORT_API_KEY = '<Your API developers key>'
    GSHEETS_IMPORT_CLIENT_ID = '<Your OAuth Client ID>'

The package is now ready to be used with your Django project.




Features and usage
==================

The ``django-gsheets-import`` package presented here strongly relies on the functionality provided by the ``django-import-export`` package.
It extends that package by the option to allow the user to import data from their Google Sheets via the Django admin.
The usage of ``django-gsheets-import`` is very similar to that of ``django-import-export``, which is nicely documented `here <https://django-import-export.readthedocs.io/en/latest/>`_.
It might also be instructive to have a look at the example Django project that ships with ``django-gsheets-import`` (see :doc:`here <demo_app>` for more details).

In short, integrating the Google Sheets import feature offered by ``django-gsheets-import`` into your Django project's admin site is a two-step process:

* Define a **resource** which determines how the fields of a given model translate to their import (and export) representations.
* Define the **admin interface** of the considered model as a subclass of ``ImportGoogleModelAdmin`` or any of the other classes provided by the package's ``admin`` submodule, namely ``ImportGoogleMixin``, ``ImportGoogleExportModelAdmin``, and ``ImportGoogleExportMixin``.


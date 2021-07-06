# django-gsheets-import

The `django-gsheets-import` package is a Django application to facilitate data import from Google Sheets within Django's admin framework.
It extends the great [`django-import-export`](https://github.com/django-import-export/django-import-export) package, which already provides import and export capabilities for all local file formats supported by [`tablib`](https://github.com/jazzband/tablib).
Exporting data from Django's admin to Google Sheets is currently not supported but planned for a future release.

Below, we briefly outline how to install and use the package.
A more detailed documentation about `django-gsheets-import` is available [here](https://django-gsheets-import.readthedocs.io/en/latest/).



## Installation and configuration

The package and its dependencies can be installed from PyPI via `pip install -U django-gsheets-import`.
To use the package in your Django project, just add `import_export` and `gsheets_import` to the list of **installed apps** in your `settings.py`, i.e.
```python
## in settings.py
INSTALLED_APPS = [
    ...,
    'import_export',
    'gsheets_import',
    ...
]
```
In order for `django-gsheets-import` to work properly, it needs to be associated with an underlying **Google Cloud Project** (GCP).
How to properly set up an appropriate GCP using the Google Cloud Console is described in more detail in the corresponding section of our [documentation](https://django-gsheets-import.readthedocs.io/en/latest/user_manual/google_cloud_project.html).
At this point, let us just note that all of the services needed are available in Google Cloud's [Free Tier](https://cloud.google.com/free/), so that there is no need to set up a billing account.
Assuming that a suitable GCP already exists, go to the [Google Cloud Console](https://console.cloud.google.com/) and navigate to `APIs & Services > Credentials`.
From there, copy an **API key**, as well as the desired **OAuth Client ID** and add them to your `settings.py`.
The required **project number** can be found under `IAM & Admin > Settings` and must also be added to `settings.py`, i.e.
```python
## in settings.py
GSHEETS_IMPORT_API_KEY = '<Your API developers key>'
GSHEETS_IMPORT_CLIENT_ID = '<Your OAuth Client ID>'
GSHEETS_IMPORT_APP_ID = '<Your project number>'
```
The package is now ready to be used with your Django project.



## Features and usage

The `django-gsheets-import` package presented here strongly relies on the functionality provided by the `django-import-export` package.
It extends that package by the option to allow the user to import data from their Google Sheets via the Django admin.
The usage of `django-gsheets-import` is very similar to that of `django-import-export`, which is nicely documented [here](https://django-import-export.readthedocs.io/en/latest/).
It might also be instructive to have a look at the example Django project that ships with `django-gsheets-import` (see the [documentation](https://django-gsheets-import.readthedocs.io/en/latest/user_manual/demo_app.html) for more details).

In short, integrating the Google Sheets import feature offered by `django-gsheets-import` into your Django project's admin site is a two-step process:

* Define a **resource** which determines how the fields of a given model translate to their import (and export) representations.
* Define the **admin interface** of the considered model as a subclass of `ImportGoogleModelAdmin` or any of the other classes provided by the package's `admin` submodule, namely `ImportGoogleMixin`, `ImportGoogleExportModelAdmin`, and `ImportGoogleExportMixin`.

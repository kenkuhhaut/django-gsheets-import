====================
The demo application
====================


In order to demonstrate the Google Sheets import feature provided by the ``django-gsheets-import`` package, the code ships with a small Django project whose admin interface uses the import functionality. It can be found in the ``tests/testapp/`` subfolder.
In the following, we briefly sketch how to run the demo project and use it for testing the import feature.



Setting up the Django project
=============================

Assuming that Python and pip have already been installed globally or in an appropriate virtual environment (recommended), the demo project can be set up by following the steps listed below.

.. code-block:: bash

    ## go to the project folder
    cd tests/testapp/

    ## install the required dependencies
    pip install -r requirements.txt

    ## prepare the database
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py loaddata authors works

    ## run the development server
    python manage.py runserver



Getting the demo sheet
======================

We have prepared a read-only sample Google Sheet, which is publicly available `here <https://docs.google.com/spreadsheets/d/1-VADSGcNxWWbhZxkhpgKZS59lTh6GDJtoriHKaE5arY/edit?usp=sharing>`__.
It contains two tables in two subsheets, one appropriate for each model in the demo project.
In order to use the sample sheet, click on the above link and sign in with your favorite Google Account (if you haven't done so already).
The demo sheet should then automatically be available from that account's Google Drive.



Setting up a Google Cloud Project
=================================

As previously mentioned, the interaction between Django and the user's Google Drive is facilitated by an underlying Google Cloud Project (GCP).
For now, you will have to create such a project yourself in order to use it with the demo application.
This is possible with every standard Google Account, does not incur any additional costs and should not take more than a couple of minutes.
The exact steps to create and set up a GCP for use with ``django-gsheets-import`` are outlined :doc:`here <google_cloud_project>`.
Once the GCP is ready, you need to retrieve your project's API key, OAuth client ID, and project number and add them to the demo application's configuration file, specifically

.. code-block:: python

    ## in tests/testapp/settings.py
    GSHEETS_IMPORT_API_KEY = '<Your API developers key>'
    GSHEETS_IMPORT_CLIENT_ID = '<Your OAuth Client ID>'
    GSHEETS_IMPORT_APP_ID = '<Your project number>'



Running the demo app
====================

Testing the import feature using the demo app typically amounts to the following steps:

* Navigate to ``http://localhost:8000`` in your browser and sign in as the Django project's superuser you created above.
* Both of the models in the project's ``literature`` app were supplemented by the Google Sheets import functionality. Choose one of the models from the sidebar, which brings you to the admin's changelist view. Here, click on the ``IMPORT`` button in the top right corner.
* The ``Google Sheet`` format is already pre-selected, so click on the ``Select a file...`` button.
* From the pop-up window, select the same Google Account which you used to access the sample sheets above.
* Grant your previously created Google Cloud Project the necessary rights when prompted.
* Select the appropriate Google Sheet from the Google Picker window.
* Click on the ``SUBMIT`` button.
* If you like what you see, click on the ``CONFIRM IMPORT`` button to have the displayed data added to the underlying database.



Further information on the demo app
===================================

Here, we compile a few more details on the demo project and its implementation.

* As mentioned above, the import functionality was added to both of the models in our demo app. Correspondingly, if you have a look at ``literature/admin.py``, you will find that both the ``AuthorAdmin`` class and the ``WorkAdmin`` class inherit from ``ImportGoogleModelAdmin``.
* Otherwise, the main work is in implementing an appropriate import resource class for each model, which is done in ``literature/resources.py``. A minimal implementation is used for the ``AuthorResource`` class, while a bit more customization was performed in writing the ``WorkResource`` class. Much more on import resources can be found in the `documentation <https://django-import-export.readthedocs.io/en/latest/>`_ of the ``django-import-export`` package.


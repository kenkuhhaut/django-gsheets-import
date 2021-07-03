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



Getting the demo sheets
=======================

We have prepared two read-only sample Google Sheets (one for each model in the demo project), which are publicly available `here <https://docs.google.com/spreadsheets/d/1DG_mR9hYRiVMt_BYIf2zc0fncFhgFQzLKplwHhEM61Q/edit?usp=sharing>`__ and `here <https://docs.google.com/spreadsheets/d/1dIPYFu0alGeAZzFh0E9y4TfnPU7Z4iqlsdh_sLdyZyA/edit?usp=sharing>`__.
In order to use them with the demo project, click on the links and sign in with your favorite Google Account (if you haven't done so already).
The demo sheets should then automatically be available from that account's Google Drive.



Running the demo app
====================

Testing the import feature using the demo app typically amounts to the following steps:

* Navigate to ``http://localhost:8000`` in your browser and sign in as the Django project's superuser you created above.
* Both of the models in the project's ``literature`` app were supplemented by the Google Sheets import functionality. Choose one of the models from the sidebar, which brings you to the admin's changelist view. Here, click on the ``IMPORT`` button in the top right corner.
* The ``Google Sheet`` format is already pre-selected, so click on the ``Select a file...`` button.
* From the pop-up window, select the same Google Account which you used to access the sample sheets above.
* Grant the **Django GSheets Import Demo** application the necessary rights.
* Select the appropriate Google Sheet from the Google Picker window.
* Click on the ``SUBMIT`` button.
* If you like what you see, click on the ``CONFIRM IMPORT`` button to have the displayed data added to the underlying database.



Further information on the demo app
===================================

Here, we compile a few more details on the demo project and its implementation.

* As mentioned above, the import functionality was added to both of the models in our demo app. Correspondingly, if you have a look at ``literature/admin.py``, you will find that both the ``AuthorAdmin`` class and the ``WorkAdmin`` class inherit from ``ImportGoogleModelAdmin``.
* Otherwise, the main work is in implementing an appropriate import resource class for each model, which is done in ``literature/resources.py``. A minimal implementation is used for the ``AuthorResource`` class, while a bit more customization was performed in writing the ``WorkResource`` class. Much more on import resources can be found in the `documentation <https://django-import-export.readthedocs.io/en/latest/>`_ of the ``django-import-export`` package.
* For the sake of convenience, the Google Sheets import feature in the demo app is by default configured to use an already existing Google Cloud Project named **Django GSheets Import Demo**. If you experience any issues with said default project, it may be due to the fact that you have to share quota with other users. In this case, create your own Google Cloud Project as described above.
* Under *no* circumstances should you use the aforementioned default Google Cloud Project for your own apps. Rather, you should create a new Google Cloud Project using your own Google Account. Note that all of the Google services needed for the ``django-gsheets-import`` feature to work properly are available within Google Cloud's `Free Tier <https://cloud.google.com/free/>`_. The correct setup is a matter of minutes.



Privacy policy
==============

The administrative interface of the demo app (the "App") provides a feature which allows users to import sample data stored in their Google Sheets into the App.
Said feature relies on Google's `Sheets API <https://developers.google.com/sheets/api/>`_ as well as on the `Picker API <https://developers.google.com/picker/docs>`_.
It uses internal resources owned by the **Django GSheets Import Demo** project (the "Project") which is hosted on Google's Cloud Platform.
The aforementioned project name is the one displayed in the consent screen during authentication.

No data about the user's Google account is shared with the App's host, the Project's owners, or any other servers.
In particular, the user's account password is never transferred to the App or the Project.
Instead, Google's OAuth server is employed to perform user authentication.

The contents of the selected Google Sheet is transferred to the memory of the App's host and, upon confirmation, permanently stored to the App's database.
If the import is not confirmed or otherwise aborted, the sheet's contents is not written to the App's database.
Meta information about the selected Google Sheet, such as its name and the names of its subsheets, are shared with the App's host, but not permanently stored.
Importantly, during each import process the user grants the described access rights only to the specific Google Sheet selected via the Google Picker dialog.
No data or metadata about the selected Google Sheet is shared with the Project.


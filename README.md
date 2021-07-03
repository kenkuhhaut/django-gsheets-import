# django-gsheets-import

The `django-gsheets-import` package is a Django application to facilitate data import from Google Sheets within Django's admin framework.
It extends the great [`django-import-export`](https://github.com/django-import-export/django-import-export) package, which already provides import and export capabilities for all local file formats supported by [`tablib`](https://github.com/jazzband/tablib).
Exporting data from Django's admin to Google Sheets is currently not supported but planned for a future release.



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
How to properly set up an appropriate GCP using the Google Cloud Console is described in more detail in the corresponding section.
At this point, let us just note that all of the services needed are available in Google Cloud's [Free Tier](https://cloud.google.com/free/), so that there is no need to set up a billing account.
Assuming that a suitable GCP already exists, go to the [Google Cloud Console](https://console.cloud.google.com/) and navigate to `APIs & Services > Credentials`.
From there, copy the **project number**, an **API key**, as well as the desired **OAuth Client ID** and add them to your `settings.py`, i.e.
```python
## in settings.py
GSHEETS_IMPORT_APP_ID = '<Your project number>'
GSHEETS_IMPORT_API_KEY = '<Your API developers key>'
GSHEETS_IMPORT_CLIENT_ID = '<Your OAuth Client ID>'
```
The package is now ready to be used with your Django project.



## Features and usage

The `django-gsheets-import` package presented here strongly relies on the functionality provided by the `django-import-export` package.
It extends that package by the option to allow the user to import data from their Google Sheets via the Django admin.
The usage of `django-gsheets-import` is very similar to that of `django-import-export`, which is nicely documented [here](https://django-import-export.readthedocs.io/en/latest/).
It might also be instructive to have a look at the example Django project that ships with `django-gsheets-import` (see below).

In short, integrating the Google Sheets import feature offered by `django-gsheets-import` into your Django project's admin site is a two-step process:

* Define a **resource** which determines how the fields of a given model translate to their import (and export) representations.
* Define the **admin interface** of the considered model as a subclass of `ImportGoogleModelAdmin` or any of the other classes provided by the package's `admin` submodule, namely `ImportGoogleMixin`, `ImportGoogleExportModelAdmin`, and `ImportGoogleExportMixin`.



## Setting up a Google Cloud Project

In order to facilitate the interaction of the `django-gsheets-import` package with the Google Cloud, one generally proceeds in three steps, specifically:

1. Create a **Google Cloud Project**.
2. Enable the required Google **APIs**, namely the Sheets API as well as the Picker API.
3. Create and download the required **keys and identifiers** related to those APIs and the user authentication workflow.

In the following, we will give step-by-step instructions to complete all of these tasks.


### Create a Google Cloud Project

* Go to the Google Cloud Console at [https://console.cloud.google.com](https://console.cloud.google.com) and sign in with the relevant Google account (e.g. a simple Gmail account).
* In the top navigation bar, click on `Select a project` (if you haven't created a project before), or on the name of the currently selected project or organization.
* Click on `NEW PROJECT` in the following dialog box.
* Choose a project name, an organization, and a corresponding location. Confirm your choices by a click on the `CREATE` button.
* Note that the project does *not* need to be linked to a billing account, see `Main Menu > Billing`.


### Enable APIs

* Navigate to `Main Menu > APIs & Services > Library` and select the API you want to enable.
* For the `django-gsheets-import` package to work properly, you need to enable the **Google Sheets API** as well as the **Google Picker API**.
* After selecting an API from the library and clicking on the `ENABLE` button, you are redirected to an overview page for this API. You can later come back to this page by going to `Main Menu > APIs & Services > Dashboard` and then selecting the API of interest from the table on the bottom.
* The aforementioned table lists all of the APIs that are currently enabled for your project. This includes several APIs that are enabled by default (cf. [here](https://cloud.google.com/service-usage/docs/enabled-service#default) in the official documentation), but are not needed for our purposes. It may be wise to disable all of the APIs that are not explicitly needed.
At least the `django-gsheets-import` package still works with all but the Sheets and Picker APIs disabled.


### Obtain credentials

* The use of the Google Picker API requires the creation of an **API key**.
  * Navigate to `Main Menu > APIs & Services > Credentials` and click on `CREATE CREDENTIALS` at the top.
  * Restrictions for the newly created API key do not have to be added for the package to work, but should still be implemented for security reasons. Under `Application restrictions`, select `HTTP referrers (websites)` and add an appropriate URL under `Website restrictions`. Under `API restrictions`, select `Restrict key` and choose the Google Picker API from the dropdown menu. The Sheets API does not need the API key and thus does not need to be selected.
* The implementation of a proper authentication and authorization workflow requires the creation of **OAuth credentials**. Obtaining those is a two-step process: First, we need to configure the OAuth consent screen. Second, we need to create an appropriate OAuth 2.0 client ID.
  1. To configure the **consent screen**, go to `Main Menu > APIs & Services > OAuth consent screen`.
      * As `User Type` you typically want to choose `External`. Click on `CREATE` and fill out the needed information.
      * For `django-gsheets-import` to work properly, you need to add the (non-sensitive) `.../auth/drive.file` scope connected to the Google Sheets API in the next step.
      * Add the email addresses of one or more test users with a valid Google account.
      * To eventually remove the restriction on the number of (test) users, you may want to have your app verified by Google. For more information on the verification process, see [here](https://support.google.com/cloud/answer/9110914), while details on unverified apps can be found [here](https://support.google.com/cloud/answer/7454865).
  2. To create an **OAuth 2.0 client ID**, go to `Main Menu > APIs & Services > Credentials` and click on `CREATE CREDENTIALS` at the top.
      * Select `Web application` as `Application type`.
      * Set the `Authorised JavaScript Origin` to `<Domain>`, where `<Domain>` is typically `http://localhost:8000` for local testing with the Django development server, or your deployment domain under which your web application is reachable. You can also add multiple relevant URIs here.
* Accessing the selected Google Sheet while only using the non-sensitive `.../auth/drive.file` scope requires the project's **App ID** to be set. It is automatically created with each Google Cloud Project and can be found as `Project number` on your project's dashboard or under the same name at `Main Menu > IAM & Admin > Settings`.



# The demo application

In order to demonstrate the Google Sheets import feature provided by the `django-gsheets-import` package, the code ships with a small Django project whose admin interface uses the import functionality. It can be found in the `tests/testapp/` subfolder.
In the following, we briefly sketch how to run the demo project and use it for testing the import feature.


## Setting up the Django project

Assuming that Python and pip have already been installed globally or in an appropriate virtual environment (recommended), the demo project can be set up by following the steps listed below.
```bash
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
```


## Getting the demo sheets

We have prepared two read-only sample Google Sheets (one for each model in the demo project), which are publicly available [here](https://docs.google.com/spreadsheets/d/1DG_mR9hYRiVMt_BYIf2zc0fncFhgFQzLKplwHhEM61Q/edit?usp=sharing) and [here](https://docs.google.com/spreadsheets/d/1dIPYFu0alGeAZzFh0E9y4TfnPU7Z4iqlsdh_sLdyZyA/edit?usp=sharing).
In order to use them with the demo project, click on the links and sign in with your favorite Google Account (if you haven't done so already). The demo sheets should then automatically be available from that account's Google Drive.


## Running the demo app

Testing the import feature using the demo app typically amounts to the following steps:

* Navigate to `http://localhost:8000` in your browser and sign in as the Django project's superuser you created above.
* Both of the models in the project's `literature` app were supplemented by the Google Sheets import functionality. Choose one of the models from the sidebar, which brings you to the admin's changelist view. Here, click on the `IMPORT` button in the top right corner.
* The `Google Sheet` format is already pre-selected, so click on the `Select a file...` button.
* From the pop-up window, select the same Google Account which you used to access the sample sheets above.
* Grant the **Django GSheets Import Demo** application the necessary rights.
* Select the appropriate Google Sheet from the Google Picker window.
* Click on the `SUBMIT` button.
* If you like what you see, click on the `CONFIRM IMPORT` button to have the displayed data added to the underlying database.



## Further information on the demo app

Here, we compile a few more details on the demo project and its implementation.

* As mentioned above, the import functionality was added to both of the models in our demo app. Correspondingly, if you have a look at `literature/admin.py`, you will find that both the `AuthorAdmin` class and the `WorkAdmin` class inherit from `ImportGoogleModelAdmin`.
* Otherwise, the main work is in implementing an appropriate import resource class for each model, which is done in `literature/resources.py`. A minimal implementation is used for the `AuthorResource` class, while a bit more customization was performed in writing the `WorkResource` class. Much more on import resources can be found in the [documentation](https://django-import-export.readthedocs.io/en/latest/) of the `django-import-export` package.
* For the sake of convenience, the Google Sheets import feature in the demo app is by default configured to use an already existing Google Cloud Project named **Django GSheets Import Demo**.
If you experience any issues with said default project, it may be due to the fact that you have to share quota with other users.
In this case, create your own Google Cloud Project as described above.
* Under *no* circumstances should you use the aforementioned default Google Cloud Project for your own apps. Rather, you should create a new Google Cloud Project using your own Google Account. Note that all of the Google services needed for the `django-gsheets-import` feature to work properly are available within Google Cloud's [Free Tier](https://cloud.google.com/free/). The correct setup is a matter of minutes.

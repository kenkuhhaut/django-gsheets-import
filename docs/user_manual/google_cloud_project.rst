=================================
Setting up a Google Cloud Project
=================================


In order to facilitate the interaction of the ``django-gsheets-import`` package with the Google Cloud, one generally proceeds in three steps, specifically:

1. Create a **Google Cloud Project**.
2. Enable the required Google **APIs**, namely the Sheets API as well as the Picker API.
3. Create and download the required **keys and identifiers** related to those APIs and the user authentication workflow.

In the following, we will give step-by-step instructions to complete all of these tasks.




Create a new Google Cloud Project
=================================

* Go to the Google Cloud Console at https://console.cloud.google.com and sign in with the relevant Google account (e.g. a simple Gmail account).
* In the top navigation bar, click on ``Select a project`` (if you haven't created a project before), or on the name of the currently selected project or organization.
* Click on ``NEW PROJECT`` in the following dialog box.
* Choose a project name, an organization, and a corresponding location. Confirm your choices by a click on the ``CREATE`` button.
* Note that the project does *not* need to be linked to a billing account, see ``Main Menu > Billing``.



Enable APIs
===========

* Navigate to ``Main Menu > APIs & Services > Library`` and select the API you want to enable.
* For the ``django-gsheets-import`` package to work properly, you need to enable the **Google Sheets API** as well as the **Google Picker API**.
* After selecting an API from the library and clicking on the ``ENABLE`` button, you are redirected to an overview page for this API. You can later come back to this page by going to ``Main Menu > APIs & Services > Dashboard`` and then selecting the API of interest from the table on the bottom.
* The aforementioned table lists all of the APIs that are currently enabled for your project. This includes several APIs that are enabled by default (cf. `here <https://cloud.google.com/service-usage/docs/enabled-service#default>`_ in the official documentation), but are not needed for our purposes. It may be wise to disable all of the APIs that are not explicitly needed. At least the ``django-gsheets-import`` package still works with all but the Sheets and Picker APIs disabled.



Obtain credentials
==================

* The use of the Google Picker API requires the creation of an **API key**.

  * Navigate to ``Main Menu > APIs & Services > Credentials`` and click on ``CREATE CREDENTIALS`` at the top.
  * Restrictions for the newly created API key do not have to be added for the package to work, but should still be implemented for security reasons.

    * Under ``Application restrictions``, select ``HTTP referrers (websites)`` and add an appropriate URL under ``Website restrictions``. Note that this can be skipped during local development and testing.
    * Under ``API restrictions``, select ``Restrict key`` and choose the Google Picker API from the dropdown menu. The Sheets API does not need the API key and thus does not need to be selected.

* The implementation of a proper authentication and authorization workflow requires the creation of **OAuth credentials**. Obtaining those is a two-step process: First, we need to configure the OAuth consent screen. Second, we need to create an appropriate OAuth 2.0 client ID.

  1. To configure the **consent screen**, go to ``Main Menu > APIs & Services > OAuth consent screen``.

      * As ``User Type`` you typically want to choose ``External``. Click on ``CREATE`` and fill out the needed information.
      * For ``django-gsheets-import`` to work properly, you need to add the (non-sensitive) ``.../auth/drive.file`` scope connected to the Google Sheets API in the next step.
      * Add the email addresses of one or more test users with a valid Google account.
      * To eventually remove the restriction on the number of (test) users, you may want to have your app verified by Google. For more information on the verification process, see `here <https://support.google.com/cloud/answer/9110914>`__, while details on unverified apps can be found `here <https://support.google.com/cloud/answer/7454865>`__.

  2. To create an **OAuth 2.0 client ID**, go to ``Main Menu > APIs & Services > Credentials`` and click on ``CREATE CREDENTIALS`` at the top.
  
      * Select ``Web application`` as ``Application type``.
      * Set the ``Authorised JavaScript Origin`` to ``<Domain>``, where ``<Domain>`` is typically ``http://localhost:8000`` for local testing with the Django development server, or your deployment domain under which your web application is reachable. You can also add multiple relevant URIs here.

* Accessing the selected Google Sheet while only using the non-sensitive ``.../auth/drive.file`` scope requires the project's **App ID** to be set. It is automatically created with each Google Cloud Project and can be found as ``Project number`` on your project's dashboard or under the same name at ``Main Menu > IAM & Admin > Settings``.



import csv
from io import StringIO
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from django.conf import settings
from django.contrib import admin
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import SimpleUploadedFile

from import_export.admin import ImportMixin, ExportMixin

from . import forms
from .google_sheet_format import DEFAULT_FORMATS_EXT




## list of names of required settings variables
SETTINGS_VARS = [
    'GSHEETS_IMPORT_API_KEY',
    'GSHEETS_IMPORT_CLIENT_ID',
    'GSHEETS_IMPORT_APP_ID',
]



###############################################################
#                                                             #
#  G o o g l e   S h e e t   i m p o r t   f u n c t i o n s  #
#                                                             #
###############################################################


## get the names of all subsheets within the given Google Sheet
def get_subsheets_names(service, sheet_id):
    ## extract metadata from specified sheet
    result_dict = service.spreadsheets().get(
        spreadsheetId = sheet_id
    ).execute()
    ## get the sheet name (file name)
    sheet_name = result_dict.get('properties', {}).get('title')
    ## get the names of the subsheets (tab names)
    subsheets_info = result_dict.get('sheets', None)
    if subsheets_info is not None:
        return ([info.get('properties', {}).get('title') for info in subsheets_info], sheet_name)


## download the given sheet's content as an in-memory CSV file to the server
def download_csv(service, sheet_id, subsheet_name, sheet_name):
    """
    Downloads the specified range from the specified Google Sheet to an in-memory CSV file.
    """
    ## extract data from specified sheet
    result = service.spreadsheets().values().get(spreadsheetId = sheet_id, range = subsheet_name).execute()
    ## write previously extracted data to an in-memory text stream in CSV format
    ## NB: csv.writer can only handle (unicode) text streams and no byte streams
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerows(result.get('values'))
    stream.seek(0)
    ## create and return an in-memory file object;
    ## content must be a byte string, not a unicode string; that is why we pass "stream.getvalue().encode('utf-8')" instead of simply "stream".
    return SimpleUploadedFile(
        name = sheet_name or 'tmp.csv',
        content = stream.getvalue().encode('utf-8'),
        content_type = 'txt/csv'
    )





#########################################################################
#                                                                       #
#  E x t e n s i o n   o f   t h e   I m p o r t M i x i n   c l a s s  #
#                                                                       #
#########################################################################

class ImportGoogleMixin(ImportMixin):
    ## template for import view
    import_template_name = 'admin/gsheets_import/import.html'

    ## available import formats
    formats = DEFAULT_FORMATS_EXT

    ## use the customized import template instead of the default one
    def get_import_form(self):
        return forms.CustomImportForm

    ## add additional context to the import template
    def get_import_context_data(self, **kwargs):
        context = super().get_import_context_data(**kwargs)
        gsheets_import_context = { var.lower(): getattr(settings, var, None) for var in SETTINGS_VARS }
        failed_settings_vars = [key.upper() for key, value in gsheets_import_context.items() if value is None]
        if len(failed_settings_vars) > 0:
            raise AttributeError("Variables in settings.py related to the Google Sheet import app not set correctly (" + ', '.join(failed_settings_vars) + ').')
        else:
            context.update(gsheets_import_context)
            return context


    ## extended version of the import_action method to download the specified Google Sheet in CSV format
    def import_action(self, request, *args, **kwargs):
        ## process google sheet
        if request.POST and request.POST.get('is_google') == 'true':
            ## only proceed if the required data was sent and is not empty
            if all([ (key in request.POST) and (request.POST[key] != '') for key in ['google_file_id', 'oauth_token'] ]):
                ## extract information about file ('file_id') and user authorization ('oauth_token')
                file_id = request.POST['google_file_id']
                oauth_token = request.POST['oauth_token']

                ## create sheets service using the provided OAuth 2.0 token
                creds = Credentials(oauth_token)
                sheets_service = build('sheets', 'v4', credentials=creds)

                ## extract subsheet names from selected Google Sheet
                subsheet_names, sheet_name = get_subsheets_names(sheets_service, file_id)

                ## download the specified sheet to an in-memory file
                sheet_file = download_csv(sheets_service, file_id, subsheet_names[0], sheet_name)

                ## NB: The request.FILES property cannot be set for an object of WSGIRequest;
                ## set the _files attribute instead, which might not be the most elegant way... (rather implement custom upload handler?)
                request._files = MultiValueDict({'import_file': [sheet_file]})

            ## raise exception if some data is missing +++ to be implemented +++
            else:
                pass

        ## call the parent method with the modified request object
        return super().import_action(request, *args, **kwargs)




#######################################
#                                     #
#  A d d i t i o n a l   m i x i n s  #
#                                     #
#######################################

class ImportGoogleExportMixin(ImportGoogleMixin, ExportMixin):
    ## template for change list view
    change_list_template = 'admin/import_export/change_list_import_export.html'




#####################################################
#                                                   #
#  S u b c l a s s e s   o f   M o d e l A d m i n  #
#                                                   #
#####################################################

class ImportGoogleModelAdmin(ImportGoogleMixin, admin.ModelAdmin):
    pass

class ImportGoogleExportModelAdmin(ImportGoogleExportMixin, admin.ModelAdmin):
    pass

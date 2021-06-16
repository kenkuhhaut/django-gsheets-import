from tablib import import_set
from import_export.formats import base_formats



##
## Format class to import Google Sheets
##
class GoogleSheet(base_formats.Format):
    def get_title(self):
        return 'Google Sheet'

    def create_dataset(self, in_stream):
        return import_set(in_stream, format='csv')

    def get_content_type(self):
        return 'application/vnd.google-apps.spreadsheet'

    def can_import(self):
        return True

    def is_binary(self):
        return False

    def get_read_mode(self):
        return 'r'



## List of default formats unconditionally extended by the Google Sheet format class
DEFAULT_FORMATS_EXT = [GoogleSheet, ] + base_formats.DEFAULT_FORMATS

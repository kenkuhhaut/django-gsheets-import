from django.contrib import admin
from gsheets_import.admin import ImportGoogleModelAdmin
from .models import Author, Work
from .resources import AuthorResource, WorkResource



##
## Admin interface for the Author model
##
class AuthorAdmin(ImportGoogleModelAdmin):
    resource_class = AuthorResource



##
## Admin interface for the Work model
##
class WorkAdmin(ImportGoogleModelAdmin):
    resource_class = WorkResource
    import_example_sheet_link = 'https://docs.google.com/spreadsheets/d/1-VADSGcNxWWbhZxkhpgKZS59lTh6GDJtoriHKaE5arY/edit#gid=1386862396'



#############################
#  R e g i s t r a t i o n  #
#############################
admin.site.register(Author, AuthorAdmin)
admin.site.register(Work, WorkAdmin)

from django.contrib import admin

from gsheets_import.admin import ImportGoogleModelAdmin

from .models import Work, Author
from .resources import WorkResource



##
## Admin interface for the Work model
##
class WorkAdmin(ImportGoogleModelAdmin):
    resource_class = WorkResource



#############################
#  R e g i s t r a t i o n  #
#############################
admin.site.register(Work, WorkAdmin)
admin.site.register(Author)

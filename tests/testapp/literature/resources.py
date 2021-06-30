from import_export import resources
from .models import Work




##
## import resources for Work model
##
class WorkResource(resources.ModelResource):
    class Meta:
        model = Work


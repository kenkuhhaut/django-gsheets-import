from import_export import resources
from import_export.fields import Field
from import_export.widgets import Widget, ForeignKeyWidget
from .models import Author, Work




###########################################################
#                                                         #
#  C u s t o m i z e d   r e s o u r c e   w i d g e t s  #
#                                                         #
###########################################################


##
## Custom widget for choice fields
##
class ChoicesWidget(Widget):
    def __init__(self, model, field, render_labels=True, *args, **kwargs):
        self.model = model
        self.field = field
        self.render_labels = render_labels
        choices = self.model._meta.get_field(self.field).choices
        self.value_to_label_map = dict(choices)
        self.label_to_value_map = {label: value for value, label in choices}
        super().__init__(*args, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value, row, *args, **kwargs)
        try:
            return self.label_to_value_map[val]
        except KeyError:
            return val

    def render(self, value, obj=None):
        if self.render_labels:
            return getattr(obj, 'get_{}_display'.format(self.field))()
        else:
            return value




###################################
#                                 #
#  M o d e l   r e s o u r c e s  #
#                                 #
###################################


##
## Import resources for Author model
##
class AuthorResource(resources.ModelResource):
    class Meta:
        model = Author



##
## Import resources for Work model
##
class WorkResource(resources.ModelResource):
    title = Field(attribute = 'title', column_name = 'Title')
    author = Field(
        attribute = 'author', column_name = 'Author',
        widget = ForeignKeyWidget(Author, field='short_name')
    )
    publication_date = Field(attribute = 'publication_date', column_name = 'Publication year')
    form = Field(
        attribute = 'form', column_name = 'Literary form',
        widget = ChoicesWidget(Work, field='form')
    )
    wiki_link = Field(attribute = 'wiki_link', column_name = 'Wikipedia link')

    class Meta:
        model = Work

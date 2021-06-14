##
## Copyright (c) 2021, Alexander Helmboldt
##
##
## This file incorporates work covered by the following copyright and  
## permission notice:
##
## Copyright (c) Bojan Mihelac and individual contributors.
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without modification,
## are permitted provided that the following conditions are met:
##
##     1. Redistributions of source code must retain the above copyright notice,
##        this list of conditions and the following disclaimer.
##
##     2. Redistributions in binary form must reproduce the above copyright
##        notice, this list of conditions and the following disclaimer in the
##        documentation and/or other materials provided with the distribution.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
## ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
## ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
## LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##



from django import forms
from django.utils.translation import gettext_lazy as _




#################################################
#                                               #
#  C u s t o m i z e d   i m p o r t   f o r m  #
#                                               #
#################################################

## slightly modified FileInput widget to use a customized template
class FileAndGoogleInput(forms.widgets.FileInput):
    template_name = 'forms/widgets/file_and_google.html'



##
## Custom import form
##
class CustomImportForm(forms.Form):
    input_format = forms.ChoiceField(
        label = _('Format'),
        choices = ()
    )
    import_file = forms.FileField(
        label = _('File to import'),
        widget = FileAndGoogleInput
    )

    def __init__(self, import_formats, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for i, fmt in enumerate(import_formats):
            choices.append( (str(i), fmt().get_title()) )
        self.fields['input_format'].choices = choices

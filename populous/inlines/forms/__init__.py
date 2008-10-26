from django import forms
from widgets import ForeignKeyRawIdWidget, InlineTextareaWidget

class InlineForm(forms.Form):
    def render(self, request):
        # TODO: finish this
        return None
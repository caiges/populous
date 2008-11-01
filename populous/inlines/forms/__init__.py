from django import forms
from django.template import Context, Template
from widgets import ForeignKeyRawIdWidget, InlineTextareaWidget

INLINE_FORM_TEMPLATE = Template("""
<form>
{% for field in form %}
{{ field.label_tag }} {{ field }}
{% endfor %}
</form>
""")

class InlineForm(forms.Form):
    def render(self, request):
        c = Context({'form': self})
        return INLINE_FORM_TEMPLATE.render(c)
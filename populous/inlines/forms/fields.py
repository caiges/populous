from django import forms
from populous.utils.validators import RelaxNGValidator
from populous.inlines.forms.widgets import InlineTextareaWidget
from populous.inlines.utils import get_absolute_schema_path, html_to_unicode

class InlineField(forms.CharField):
    def __init__(self, schema_path, additional_root_element=None, *args, **kwargs):
        kwargs.update({'widget': InlineTextareaWidget})
        super(InlineField, self).__init__(*args, **kwargs)
        self.schema_path = schema_path
        self.additional_root_element = additional_root_element
    
    def clean(self, value):
        schema_path = get_absolute_schema_path(self.schema_path)
        xml_validator = RelaxNGValidator(schema_path, self.additional_root_element)
        
        #TODO: This shouldn't be hard-coded to `content`
        value = u"<content>%s</content>" % html_to_unicode(value)
        return xml_validator.forms_validate(value)
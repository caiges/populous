"""
Custom InlineField class.
"""
from django.db import models
from populous.inlines import forms
from populous.utils.validators import RelaxNGValidator

class InlineField(models.TextField):
    def __init__(self, schema_path=None, additional_root_element=None, *args, **kwargs):
        super(InlineField, self).__init__(*args, **kwargs)
        self.additional_root_element = additional_root_element
        self.schema_path = schema_path

    def clean(self, value):
        super(XmlField, self).clean(value)
        schema_path = self.schema_path
        xml_validator = RelaxNGValidator(schema_path, self.additional_root_element)
        return xml_validator.forms_validate(value)
    
    def formfield(self, **kwargs):
        """
        We need a custom ``formfield`` because we need to ensure that
        the ``textarea`` is rendered with the proper ``InlineField``
        widget.
        """
        kwargs.update({'widget': forms.InlineTextareaWidget})
        return super(InlineField, self).formfield(**kwargs)
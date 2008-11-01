"""
Custom InlineField class.
"""
from django.db import models
from populous.inlines.forms.fields import InlineField as InlineFormField

def get_default_schema():
    return __file__.rsplit('/', 1)[0] + "/default_schema.rng"

class InlineField(models.TextField):
    def __init__(self, schema_path=None, additional_root_element=None, *args, **kwargs):
        super(InlineField, self).__init__(*args, **kwargs)
        self.additional_root_element = additional_root_element
        self.schema_path = schema_path or get_default_schema()
    
    def formfield(self, **kwargs):
        """
        We need a custom ``formfield`` because we need to ensure that
        the ``textarea`` is rendered with the proper ``InlineField``
        widget and also to add XML validation.
        """
        return InlineFormField(self.schema_path, **kwargs)
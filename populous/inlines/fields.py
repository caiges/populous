"""
Custom InlineField class.
"""
from django.db import models
from populous.inlines.forms.fields import InlineField as InlineFormField

def get_default_schema():
    #return __file__.rsplit('/', 1)[0] + "/schemas/default_schema.rng"
    return "default_schema.rng"

class InlineField(models.TextField):
    def __init__(self, schema_path=None, additional_root_element=None, *args, **kwargs):
        super(InlineField, self).__init__(*args, **kwargs)
        self.additional_root_element = additional_root_element
        self.schema_path = schema_path or get_default_schema()
    
    def contribute_to_class(self, cls, name):
        super(InlineField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self)
        
        self.app_label = cls._meta.app_label
        self.model_name = cls._meta.module_name
        
    def formfield(self, **kwargs):
        """
        We need a custom ``formfield`` because we need to ensure that
        the ``textarea`` is rendered with the proper ``InlineField``
        widget and also to add XML validation.
        """
        schema_path = "%s_%s_%s.rng" % (self.app_label, self.model_name, self.name)
        return InlineFormField(schema_path, **kwargs)
"""
Custom InlineField class.
"""
from django.db import models
from populous.inlines import forms

class InlineField(models.XMLField):
    def __init__(self, *args, **kwargs):
        super(InlineField, self).__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        """
        We need a custom ``formfield`` because we need to ensure that
        the ``textarea`` is rendered with the proper ``InlineField``
        widget.
        """
        kwargs.update({'widget': forms.InlineTextareaWidget})
        return super(InlineField, self).formfield(**kwargs)
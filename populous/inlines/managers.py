from django.db import models
from django.utils.encoding import force_unicode
from django.template.defaultfilters import capfirst
from populous.inlines.utils import get_inline_description

class RegisteredInlineManager(models.Manager):
    def get_inline(self, *args, **kwargs):
        """
        Works just like the normal ``get`` method, however, this
        returns the actual ``Inline`` subclass; *NOT* a 
        ``RegisteredInline`` model.
        """
        reged_inline = self.get(*args, **kwargs)
        return reged_inline.get_inline()
        
    def create_from_inline(self, inline):
        app_label = inline.app_label
        class_name = inline.__class__.__name__
        
        try:
            obj = self.get(app_label=app_label, class_name=class_name)
            return (obj, False)
        except self.model.DoesNotExist:
            doc = get_inline_description(inline)
            obj = self.create(
                name=capfirst(force_unicode(getattr(inline, 'verbose_name'))),
                description=force_unicode(getattr(inline, 'description', doc)),
                author=force_unicode(getattr(inline, 'author', '')),
                app_label=force_unicode(app_label),
                class_name=force_unicode(class_name),
                inline_name=force_unicode(inline.name)
            )
            return (obj, True)

class RegisteredInlineFieldManager(models.Manager):
    def create_from_field(self, model_class, field):
        app_label=model_class._meta.app_label
        model_name=model_class._meta.module_name
        field_name=field.name
        return self.get_or_create(app_label=app_label, model_name=model_name, field_name=field_name)
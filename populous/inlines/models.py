from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template.defaultfilters import capfirst

from populous.inlines.managers import RegisteredInlineManager, RegisteredInlineFieldManager
from populous.inlines.utils import get_absolute_schema_path


class RecurringInline(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(help_text='Raw HTML is allowed.')
    
    class Meta:
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title

class RegisteredInline(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=800, blank=True)
    
    app_label = models.CharField(max_length=500, editable=False)
    class_name = models.CharField(max_length=500, editable=False)
    inline_name = models.SlugField(max_length=500, editable=False)
    
    objects = RegisteredInlineManager()
    
    class Meta:
        verbose_name = 'inline'
        unique_together = (('app_label', 'class_name', 'inline_name'),)
    
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_form_url(self):
        return ('inlines-admin-form', (), {
            'app_label': self.app_label,
            'inline_name': self.inline_name})

    @property    
    def inline_class(self):
        if not hasattr(self, '_inline_class'):
            app_name = models.get_app(self.app_label).__name__
            mod_name = "%sinlines" % app_name.rstrip('models')
            mod = __import__(mod_name, fromlist=[mod_name])
            setattr(self, '_inline_class', getattr(mod, self.class_name))
        return getattr(self, '_inline_class')
    
    def get_form(self):
        return self.inline_class.form
        

## TODO: Currently field-level control doesn't work.

class RegisteredInlineField(models.Model):
    app_label = models.CharField(max_length=500, editable=False)
    model_name = models.CharField(max_length=500, editable=False)
    field_name = models.CharField(max_length=500, editable=False)
    schema_path = models.CharField(max_length=800, editable=False)
    
    objects = RegisteredInlineFieldManager()
    
    class Meta:
        verbose_name = 'inline field'
        unique_together = (('app_label', 'model_name', 'field_name'),)
    
    def __unicode__(self):
        return u"%s.%s" % (capfirst(self.model_name), self.field_name)
    
    def get_absolute_schema_path(self):
        return get_absolute_schema_path(self.schema_path)
    

class AllowedField(models.Model):
    inline = models.ForeignKey(RegisteredInline)
    field = models.ForeignKey(RegisteredInlineField)
    sites = models.ManyToManyField(Site)
    
    def __unicode__(self):
        return unicode(self.field)
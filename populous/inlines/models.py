from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from populous.inlines.managers import RegisteredInlineManager, RegisteredInlineFieldManager


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
    
    objects = RegisteredInlineManager()
    
    class Meta:
        verbose_name = 'inline'
        unique_together = (('app_label', 'class_name'),)
    
    def __unicode__(self):
        return self.name

    @property    
    def inline_class(self):
        if not hasattr(self, '_inline_class'):
            app_name = models.get_app(self.app_label).__name__
            mod_name = "%sinlines" % app_name.rstrip('models')
            mod = __import__(mod_name, fromlist=[mod_name])
            setattr(self, '_inline_class', getattr(mod, self.class_name))
        return getattr(self, '_inline_class')
        
    
class RegisteredInlineField(models.Model):
    
    app_label = models.CharField(max_length=500, editable=False)
    model_name = models.CharField(max_length=500, editable=False)
    field_name = models.CharField(max_length=500, editable=False)
    
    objects = RegisteredInlineFieldManager()
    
    class Meta:
        verbose_name = 'inline field'
        unique_together = (('app_label', 'model_name', 'field_name'),)
    
    def __unicode__(self):
        return u"%s: %s" % (self.model_name, self.field_name)
    

class AllowedField(models.Model):
    inline = models.ForeignKey(RegisteredInline)
    field = models.ForeignKey(RegisteredInlineField)
    sites = models.ManyToManyField(Site)
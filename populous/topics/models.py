from django.db import models
from django.utils.translation import ugettext_lazy as _

from populous.categories.models import Category
from populous.filebrowser.fields import FileBrowseField

class Topic(models.Model):
    name     = models.CharField(_('name'), max_length=100)
    slug     = models.SlugField(_('slug'), unique=True)
    url      = models.CharField(_('URL'), max_length=500, blank=True)
    category = models.ForeignKey(Category, verbose_name=_('category'), limit_choices_to={'representation__istartswith': 'topics'})
    image    = FileBrowseField(_("image"), max_length=500, initial_directory='/topics/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True)
    
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('topics-detail', [self.slug])
    
    def get_similar_topics(self):
        return self._default_manager.filter(category=self.category).exclude(pk=self.pk)

class TopicCollection(models.Model):
    url    = models.CharField(_('URL'), max_length=500, blank=True)
    topics = models.ManyToManyField(Topic)
    
    def __unicode__(self):
        return "Topic Collection for %s" % self.url

    def save(self, force_insert=False, force_update=False):
        print self.url[-1]
        if self.url[-1] != u'/':
            # raise ValidationError
            self.url = self.url + u'/'
        super(TopicCollection, self).save(force_insert, force_update)
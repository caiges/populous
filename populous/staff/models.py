from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from populous.categories.models import Category
from populous.filebrowser.fields import FileBrowseField

class StaffMember(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    blurb = models.TextField(_('blurb'), blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    mugshot = FileBrowseField(_("mugshot"), max_length=500, initial_directory='/images/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True)
    
    sites = models.ManyToManyField(Site)
    
    def __unicode__(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        else:
            return self.user.username

class Position(models.Model):
    title = models.CharField(_('title'), max_length=300)
    categories = models.ManyToManyField(Category, verbose_name=_('related categories'), blank=True)
    
    def __unicode__(self):
        return self.title

class PositionInline(models.Model):
    position = models.ForeignKey(Position)
    
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return u"%s: %s - %s" % (self.position, self.start_date, self.end_date or 'present')

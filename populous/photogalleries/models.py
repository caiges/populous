from django.db import models
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from populous.media.models import Audio, Photo

class Gallery(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'))
    description = models.TextField(_('description'), blank=True)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)
    template_prefix = models.CharField(_('custom template prefix'), max_length=25, blank=True,
        help_text=_("Enter only the prefix used in your template names. The system will substitute the prefix automatically. i.e. 'galleries/PREFIX_detail.html'."))
    audio = models.ForeignKey(Audio, verbose_name=_('audio'), blank=True, null=True,
        help_text=_("Audio to accompany the slideshow."))
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    
    # Managers
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    
    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')
        ordering = ('-date_created',)
        unique_together = ('slug', 'date_created')
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def get_absolute_url(self):
        return u"/media/galleries/%s/" % self.slug

class GalleryPhoto(models.Model):
    gallery = models.ForeignKey(Gallery)
    photo = models.ForeignKey(Photo)
    pause = models.IntegerField(blank=True, null=True, verbose_name=_("Seconds to pause"))
    
    class Meta:
        order_with_respect_to = 'gallery'
    
    def __unicode__(self):
        return repr(self.photo)
    
    def get_absolute_url(self):
        return u"%s%s/" % (self.gallery.get_absolute_url(), self.id)

class GallerySet(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    date_created = models.DateTimeField(_('date created'))
    template_name = models.CharField(_('template name'), max_length=200, blank=True,
        help_text=_("Leave off the leading slash and include the trailing '.html'. Example: 'photogalleries/sports_set_detail.html'. The system will use 'media/gallerysets_detail.html' by default."))
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    
    # Managers
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    
    class Meta:
        verbose_name = _('gallery set')
        verbose_name_plural = _('gallery sets')
        ordering = ('-date_created',)
    
    def __unicode__(self):
        return u"%s" % self.name
    
    def get_absolute_url(self):
        return u"/media/galleries/sets/%s/" % self.slug
    
    def get_first_gallery(self):
        _("Small optimization that returns the first gallery in this set and caches it")
        if not hasattr(self, "_first_gallery_cache"):
            from django.conf import settings
            self._first_gallery_cache = self.gallery_set.filter(sites__id__exact=settings.SITE_ID)[0]
        return self._first_gallery_cache
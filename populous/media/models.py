from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site

from populous.filebrowser.fields import FileBrowseField
from populous.staff.models import StaffMember
from populous.categories.models import Category

CONTENT_TYPE_CHOICES = (
    ('audio', 'Audio'),
    ('document', 'Document'),
    ('file', 'File'),
    ('image', 'Photo or Image'),
    ('other', 'Other'),
    ('podcast', 'Podcast'),
    ('video', 'Video'),

)

class BaseFileType(models.Model):
    name = models.CharField(_('name'), max_length=100)
    mime_type = models.CharField(_('mime-type'), max_length=200)
    content_type = models.CharField(_('content type'), max_length=20, choices=CONTENT_TYPE_CHOICES)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.content_type)

###############
# Audio Media #
###############
class Audio(models.Model):
    title = models.CharField(_('title'), max_length=255)
    type = models.ForeignKey(BaseFileType, limit_choices_to={'content_type': 'audio'}, verbose_name=_('audio type'))
    file = FileBrowseField(_('audio file'), initial_directory='/audio/', blank=True, null=True)
    url = models.URLField(_('audio URL'), blank=True, null=True)
    date_created = models.DateTimeField(_('date created'))
    date_uploaded = models.DateTimeField(_('date updated'), auto_now_add=True)
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True, null=True)
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    
    # Managers
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    
    class Meta:
        verbose_name_plural = _("audio")
        get_latest_by = "date_created"
    
    def __unicode__(self):
        return self.title
    
    def mime_type(self):
        _("""Return the correct mime-type for an video file depending on its audio_type""")
        return u"%s" % self.type.mime_type
    
    def get_audio_url(self):
        if self.file:
            return self.file
        else:
            return self.url

##############
# Misc Files #
##############
class File(models.Model):
    title = models.CharField(_('title'), max_length=500)
    type = models.ForeignKey(BaseFileType, limit_choices_to={'content_type': 'file'}, verbose_name=_('file type'))
    file = models.FileField(_('file'), upload_to='files/%Y/%m/%d', blank=True, null=True)
    date_uploaded = models.DateTimeField(_('date updated'), auto_now_add=True)
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True, null=True)
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    
    # Managers
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    
    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        ordering = ('title',)
        get_latest_by = "date_uploaded"
    
    def mime_type(self):
        _("""Return the correct mime-type for a file depending on its file_type""")
        return u"%s" % self.type.mime_type

##########
# Photos #
##########
class Photo(models.Model):
    type = models.ForeignKey(BaseFileType, limit_choices_to={'content_type': 'image'}, verbose_name=_('file type'))
    file = models.ImageField(_('image file'), upload_to='img/images/%Y/%m/%d', width_field='width', height_field='height',
        help_text=_('Photos must ONLY be of the file formats including: jpg|gif|png'))
    width = models.IntegerField(_('width'), blank=True, null=True, editable=False)
    height = models.IntegerField(_('height'), blank=True, null=True, editable=False)
    caption = models.TextField(_('caption'), blank=True)
    date_created = models.DateTimeField(_('date created'))
    date_uploaded = models.DateTimeField(_('date updated'), auto_now_add=True)
    photographer = models.ForeignKey(StaffMember, blank=True, null=True, limit_choices_to={'responsibilities__name__iexact': 'takes photos'}, verbose_name=_('photographer'))
    one_off_photographer = models.CharField(_('one-off photographer'), max_length=100, blank=True)
    credit = models.CharField(_('credit'), max_length=150, blank=True)
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True, null=True)
    is_sellable = models.BooleanField(_('is sellable'), default=False)
    sites = models.ManyToManyField(Site)
    
    # Managers
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')
    
    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')
        ordering = ('-date_uploaded',)
        get_latest_by = "date_created"
    
    def __unicode__(self):
        return strip_tags(self.caption).strip()[:100] or u"[%s]" % self.file.name
    
    def get_absolute_url(self):
        return u"/media/photos/%s/%s/" % (self.creation_date.strftime("%Y/%b/%d").lower(), self.id)
    
    def mime_type(self):
        _("""Return the correct mime-type for a file depending on its file_type""")
        return u"%s" % self.type.mime_type

##########
# Videos #
##########
class Video(models.Model):
    title = models.CharField(_('title'), max_length=200)
    caption = models.TextField(_('caption'), blank=True)
    date_created = models.DateTimeField(_('date created'))
    date_uploaded = models.DateTimeField(_('date uploaded'), auto_now_add=True)
    
    videographer = models.ForeignKey(StaffMember, blank=True, null=True, verbose_name=_('videographer'))
    one_off_videographer = models.CharField(_('one-off videographer'), max_length=200, blank=True)
    
    type = models.ForeignKey(BaseFileType, limit_choices_to={'content_type': 'video'}, verbose_name=_('video type'))
    file = models.FileField(_('video file'), upload_to='videos/%Y/%m/%d', blank=True, null=True)
    url = models.URLField(_('video URL'),
        help_text=_('Full URL to the video file.  Use this only if no video file is provided.'), blank=True, null=True)
    
    categories = models.ManyToManyField(Category, verbose_name='categories', blank=True, null=True)
    width = models.IntegerField(_('video width'), default=320, help_text=_('In pixels.'))
    height = models.IntegerField(_('video height'), default=240, help_text=_('In pixels.'))
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    
    thumbnail_photo = models.ImageField(_('thumbnail photo'), upload_to='videos/%Y/%m/%d',
        width_field='thumbnail_width', height_field='thumbnail_height', blank=True, null=True)
    thumbnail_width = models.IntegerField(_('thumbnail width'), blank=True, null=True, editable=False)
    thumbnail_height = models.IntegerField(_('thumbnail height'), blank=True, null=True, editable=False)
    
    # Managers
    objects = models.Manager()
    on_site = CurrentSiteManager('sites')

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        ordering = ('-date_created',)
        get_latest_by = "date_created"

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return u"/media/videos/%s/%s/" % (self.date_created.strftime("%Y/%b/%d").lower(), self.id)
    
    def get_video_url(self):
        if self.file:
            return self.file
        else:
            return self.url
    
    def mime_type(self):
        _("""Return the correct mime-type for a file depending on its file_type""")
        return u"%s" % self.type.mime_type

class AlternateVideo(models.Model):
    '''An AlternateVideo is used if you want to have multiple version of a video available.  Say for instance you want to provide multiple resolutions of the same video for different bandwidths, or if you want to provide the video in multiple formats (i.e. .flv, .avi, .mov, ...)'''
    video = models.ForeignKey(Video)
    type = models.ForeignKey(BaseFileType, limit_choices_to={'content_type': 'video'}, verbose_name=_('video type'))
    file = models.FileField(_('video file'), upload_to='videos/%Y/%m/%d', blank=True, null=True)
    url = models.URLField(_('video URL'),
        help_text=_('Full URL to the video file.  Use this only if no video file is provided.'), blank=True, null=True)
    
    width = models.IntegerField(_('video width'), default=320, help_text=_('In pixels.'))
    height = models.IntegerField(_('video height'), default=240, help_text=_('In pixels.'))

    def __unicode__(self):
        return self.video.title
    
    def get_video_url(self):
        if self.file:
            return self.file
        else:
            return self.url
    
    def mime_type(self):
        _("""Return the correct mime-type for a file depending on its file_type""")
        return u"%s" % self.type.mime_type
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from populous.categories.models import Category
from populous.filebrowser.fields import FileBrowseField
from populous.inlines.fields import InlineField
from populous.tagging.fields import TagField

BLOG_STATUS_CHOICES = (
    (0, 'Disabled'),
    (1, 'Frozen'),
    (2, 'Live'),
)

COMMENT_CHOICES = (
    (0, "Disabled"),
    (1, "Frozen"),
    (2, "Enabled"),
)

ENTRY_STATUS_CHOICES = (
    (0, 'Hidden'),
    (1, 'Draft'),
    (2, 'Live'),
)

class BlogCollection(models.Model):
    title = models.CharField(_('title'), max_length=300)
    slug = models.SlugField(_('slug'), unique=True)
    description = InlineField(verbose_name=_('description'), blank=True)
    template_name = models.CharField(_('template name'), max_length=500, blank=True)
    
    class Meta:
        verbose_name = _("blog collection")
        verbose_name_plural = _("blog collections")
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('blogs-collection', [
                self.slug,
            ]
        )

class Blog(models.Model):
    title = models.CharField(_('title'), max_length=300)
    slug = models.SlugField(_('slug'), unique=True)
    description = InlineField(verbose_name=_('description'), blank=True)
    image = FileBrowseField(_('lead photo'), max_length=500, initial_directory='/blogs/images/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True,
        help_text=_("This is the photo that shows up with the name of this blog."))
    collection = models.ForeignKey(BlogCollection, verbose_name=_('collection'), blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), blank=True, limit_choices_to={'representation__istartswith': 'blogs'})
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    default_comment_status = models.IntegerField(_('default comment status'), default=2, choices=COMMENT_CHOICES,
        help_text=_('"Disabled" will not display any comments for this blog.<br/>'
            '"Frozen" will display existing comments, but prevent the posting of new comments.<br/>'
            '"Enabled" will allow new comments.'))
    status = models.IntegerField(_('status'), choices=BLOG_STATUS_CHOICES, default=2,
        help_text=_('"Disabled" will hide the blog completely.<br/>'
            '"Frozen" will display the blog, but prevent the posting of new entries.<br/>'
            '"Enabled" will allow full function of the blog.'))
    post_entry_note = InlineField(verbose_name=_('post-entry note'), blank=True)
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    contributors = models.ManyToManyField(User, verbose_name=_('contributors'), )
    tags = TagField()
    
    # Template Overrides
    template_name_blog = models.CharField(_('blog template name'), max_length=500, blank=True)
    template_name_date_archive = models.CharField(_('date archive template name'), max_length=500, blank=True)
    template_name_entry = models.CharField(_('entry template name'), max_length=500, blank=True)
    
    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('blogs-entry_index', [
                self.slug,
            ]
        )

class Entry(models.Model):
    blog = models.ForeignKey(Blog, verbose_name=_('blog'))
    title = models.CharField(_('title'), max_length=300)
    tease = models.TextField(_('tease'), blank=True)
    entry = InlineField(verbose_name=_('entry'))
    bylines = models.ManyToManyField(User, verbose_name=_('bylines'), blank=True)
    bylines_override = models.CharField(_('byline override'), max_length=300, blank=True,
        help_text=_("If entered, no users selected in the bylines field will show up on the entry page."))
    pub_date = models.DateTimeField(_('publication date'))
    update_date = models.DateTimeField(auto_now=True)
    
    # Meta
    featured = models.BooleanField(_('featured'), default=False)
    slug = models.SlugField(_('slug'))
    tags = TagField()
    status = models.IntegerField(_('status'), choices=ENTRY_STATUS_CHOICES, default=2)
    comment_status = models.IntegerField(_('comment status'), blank=True, null=True, choices=COMMENT_CHOICES,
        help_text=_('This will override the default comment status of the blog.<br/>'
            '"Disabled" will not display any comments for this story.<br/>'
            '"Frozen" will display existing comments, but prevent the posting of new comments.<br/>'
            '"Enabled" will allow new comments.'))
    
    class Meta:
        unique_together = ("pub_date", "slug")
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.blog)
    
    @models.permalink
    def get_absolute_url(self):
        return ('blogs-entry_detail', [
                self.blog.slug,
                self.pub_date.year,
                self.pub_date.strftime('%b').lower(),
                self.pub_date.day,
                self.slug
            ]
        )
    
    def get_comment_status(self):
        if self.comment_status:
            return self.comment_status
        else:
            return self.blog.default_comment_status
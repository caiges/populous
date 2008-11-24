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

class BlogManager(models.Manager):
    def recently_updated(self):
        return Blog.objects.extra(
            select={'latest_entry': 'SELECT "blogs_entry"."pub_date" FROM "blogs_entry" WHERE "blogs_entry"."blog_id" = "blogs_blog"."id" ORDER BY "blogs_entry"."pub_date" DESC LIMIT 1'}
            ).order_by('-latest_entry')

class Blog(models.Model):
    creator = models.ForeignKey(User, editable=False)
    title = models.CharField(_('title'), max_length=300)
    slug = models.SlugField(_('slug'), unique=True)
    description = InlineField(verbose_name=_('description'), blank=True)
    image = FileBrowseField(_('lead photo'), max_length=500, initial_directory='/blogs/images/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True,
        help_text=_("This is the photo that shows up with the name of this blog."))
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
    post_entry_note = InlineField(verbose_name=_('post-entry note'), blank=True,
        help_text=_("This note will appear at the end of each entry of this blog."))
    sites = models.ManyToManyField(Site, verbose_name=_('sites'))
    contributors = models.ManyToManyField(User, related_name="blog_contributor_set", verbose_name=_('contributors'),
        help_text=_("Select the user(s) that can post new entries to this blog."))
    moderators = models.ManyToManyField(User, related_name="blog_moderator_set", verbose_name=_('moderators'),
        help_text=_("Select the user(s) that can modify this blog and all related entries.  The user(s) cannot delete this blog."))
    tags = TagField()
    
    # Template Overrides
    template_name_blog = models.CharField(_('blog template name'), max_length=500, blank=True,
        help_text=_("This template will override the blog index page.  Leave off the leading slash.  If this isn't provided, the system will default to 'blogs/entry_detail.html'<br>"
            "Example: 'blogs/entry_archive_index.html'"))
    template_name_date_archive = models.CharField(_('date archive template name'), max_length=500, blank=True,
        help_text=_("This template will override each date-based archive page. (i.e. year, month, day)  Leave off the leading slash.  If this isn't provided, the system will default to 'blogs/entry_archive_<interval>.html'<br>"
            "Example: 'blogs/my_blog_archive.html'"))
    template_name_entry = models.CharField(_('entry template name'), max_length=500, blank=True,
        help_text=_(
            "This template will override each entry page.  Leave off the leading slash.  If this isn't provided, the system will default to 'blogs/entry_detail.html'<br>"
            "Example: 'blogs/my_blog_entry_detail.html'"))
    
    objects = BlogManager()
    
    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('blogs-entry_archive', [self.slug,])

class BlogCollection(models.Model):
    title = models.CharField(_('title'), max_length=300)
    slug = models.SlugField(_('slug'), unique=True)
    description = InlineField(verbose_name=_('description'), blank=True)
    blogs = models.ManyToManyField(Blog, verbose_name=_('blogs'), blank=True, null=True)
    moderators = models.ManyToManyField(User, related_name="blog_collection_moderator_set", verbose_name=_('moderators'), blank=True, null=True)
    template_name = models.CharField(_('template name'), max_length=500, blank=True,
        help_text=_("This template will override the blog collection page.  Leave off the leading slash.  If this isn't provided, the system will default to 'blogs/collection_default.html'<br>"
            "Example: 'blogs/my_collection_template.html'"))
    
    class Meta:
        verbose_name = _("blog collection")
        verbose_name_plural = _("blog collections")
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('blogs-collection_detail', [self.slug,])

class Entry(models.Model):
    creator = models.ForeignKey(User, editable=False)
    blog = models.ForeignKey(Blog, verbose_name=_('blog'))
    title = models.CharField(_('title'), max_length=300)
    tease = models.TextField(_('tease'), blank=True)
    entry = InlineField(verbose_name=_('entry'))
    bylines = models.ManyToManyField(User, related_name="blog_entry_byline_set", verbose_name=_('bylines'), blank=True)
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
        ordering = ['-pub_date']
        unique_together = ("pub_date", "slug")
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
        get_latest_by = "pub_date"
    
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
        ])
    
    def get_comment_status(self):
        if self.comment_status:
            return self.comment_status
        else:
            return self.blog.default_comment_status
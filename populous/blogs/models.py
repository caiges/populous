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

class Blog(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = InlineField(blank=True)
    image = FileBrowseField(_("lead photo"), max_length=500, initial_directory='/blogs/images/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True,
        help_text=_("This is the photo that shows up with the name of this blog."))
    categories = models.ManyToManyField(Category, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    template_name = models.CharField(_('template name'), max_length=500, blank=True)
    default_comment_status = models.IntegerField(_('default comment status'), default=2, choices=COMMENT_CHOICES,
        help_text=_('"Disabled" will not display any comments for this story.<br/>'
            '"Frozen" will display existing comments, but prevent the posting of new comments.<br/>'
            '"Enabled" will allow new comments.'))
    status = models.IntegerField(choices=BLOG_STATUS_CHOICES, default=2)
    post_entry_note = InlineField(blank=True)
    sites = models.ManyToManyField(Site)
    contributors = models.ManyToManyField(User)
    tags = TagField()
    
    class Meta:
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.CharField(max_length=300)
    tease = InlineField(blank=True)
    entry = InlineField()
    bylines = models.ManyToManyField(User, blank=True)
    bylines_override = models.CharField(_('byline override'), max_length=300, blank=True,
        help_text=_("If entered, no users selected in the bylines field will show up on the entry page."))
    pub_date = models.DateTimeField()
    update_date = models.DateTimeField(auto_now=True)
    
    # Meta
    featured = models.BooleanField(default=False)
    slug = models.SlugField()
    tags = TagField()
    status = models.IntegerField(choices=ENTRY_STATUS_CHOICES, default=2)
    comment_status = models.IntegerField(_('comment status'), blank=True, null=True, choices=COMMENT_CHOICES,
        help_text=_('This will override the default comment status of the blog.<br/>'
            '"Disabled" will not display any comments for this story.<br/>'
            '"Frozen" will display existing comments, but prevent the posting of new comments.<br/>'
            '"Enabled" will allow new comments.'))
    
    class Meta:
        unique_together = ("pub_date", "slug")
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
    
    def get_comment_status(self):
        if self.comment_status:
            return self.comment_status
        else:
            return self.blog.default_comment_status
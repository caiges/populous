from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from populous.categories.models import Category
from populous.filebrowser.fields import FileBrowseField
from populous.inlines.fields import InlineField
from populous.staff.models import StaffMember
#from populous.tagging.fields import TagField
from populous.topics.models import Topic

COMMENT_CHOICES = (
    (0, "Disabled"),
    (1, "Frozen"),
    (2, "Enabled"),
)

class StoryManager(models.Manager):
    def approved(self):
        return super(StoryManager, self).get_query_set().filter(is_approved=True, sites=Site.objects.get_current())
    
    def on_site(self):
        return super(StoryManager, self).get_query_set().filter(sites=Site.objects.get_current())

class Dateline(models.Model):
    dateline = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name = _("dateline")
        verbose_name_plural = _("datelines")
    
    def __unicode__(self):
        return self.dateline

class Story(models.Model):
    # Content
    headline = models.CharField(_('headline'), max_length=300)
    subhead = models.CharField(_('subhead'), max_length=500, blank=True)
    tease = models.TextField(_('tease'), blank=True)
    story = InlineField()
    post_story_blurb = models.CharField(_('post-story blurb'), max_length=500, blank=True)
    
    # Media
    lead_photo = FileBrowseField(_("lead photo"), max_length=500, initial_directory='/images/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True,
        help_text=_("This is the photo that shows up at the top of the story page."))
    lead_photo_has_headline = models.BooleanField(default=False,
        help_text=_("If checked, the story's headline won't show up on the story page."))
    tease_photo = FileBrowseField(_("tease photo"), max_length=500, initial_directory='/images/', extensions_allowed=['.jpg', '.jpeg', '.gif','.png','.tif','.tiff'], blank=True, null=True,
        help_text=_("This is the photo that shows up with the tease text."))
    
    # Meta
    pub_date = models.DateTimeField()
    update_date = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), limit_choices_to={'representation__istartswith': 'stories'},
        help_text=_("You can think of these as sections in a newspaper."))
    bylines = models.ManyToManyField(StaffMember, blank=True)
    bylines_override = models.CharField(_('byline override'), max_length=300, blank=True,
        help_text=_("If entered, no staff members selected in the bylines field will show up on the story page."))
    slug = models.SlugField(_('slug'))
    #tags = TagField()
    topics = models.ManyToManyField(Topic, blank=True, null=True)
    dateline = models.ForeignKey(Dateline, verbose_name=_('dateline'), blank=True, null=True)
    is_approved = models.BooleanField(_('approved for publishing'), default=False,
        help_text=_("This must be checked for the story to be visible to the public."))
    comment_status = models.IntegerField(_('comments'), default=2, choices=COMMENT_CHOICES,
        help_text=_('"Disabled" will not display any comments for this story.<br/>'
            '"Frozen" will display existing comments, but prevent the posting of new comments.<br/>'
            '"Enabled" will allow new comments.'))
    #is_editorial = models.BooleanField(default=False) TODO Decide if this field should be kept
    sites = models.ManyToManyField(Site)
    
    objects = StoryManager()
    
    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']
        unique_together = ("pub_date", "slug")
        verbose_name = _("story")
        verbose_name_plural = _("stories")
    
    def __unicode__(self):
        return self.headline
    
    @models.permalink
    def get_absolute_url(self):
        return (
            'news-story_detail', [
                self.pub_date.year,
                self.pub_date.strftime('%b').lower(),
                self.pub_date.day,
                self.slug
            ]
        )

class AdditionalContent(models.Model):
    story = models.ForeignKey(Story)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        verbose_name = _("additional content")
        verbose_name_plural = _("additional content")
    
    def __unicode__(self):
        return u"%s" % self.content_object

class Collection(models.Model):
    title = models.CharField(_('name'), max_length=200)
    url = models.CharField(_('url'), max_length=500, unique=True)
    content = InlineField(blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name=_('category'))
    limit = models.PositiveIntegerField(_('max number of objects'), default=15,
        help_text=_("This is the maximum number of objects to display on the page.  This is used to limit the number of automatically displayed stories.  If objects are specified to be displayed manually, then additional stories will be appended automatically until the total number of objects in the collection reaches this limit.  If the number of manually specified objects exceeds this limit, no stories will be appended and all manually specified objects will be displayed."))
    start_date = models.DateTimeField(_('start date'), blank=True, null=True,
        help_text=_("If specified, this collection page will not show up until after the specified date."))
    end_date   = models.DateTimeField(_('end date'), blank=True, null=True,
        help_text=_("If specified, this collection page will not be visible after the specified date."))
    template_name = models.CharField(_('template name'), max_length=500, blank=True)
    sites = models.ManyToManyField(Site)
    
    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")
    
    def __unicode__(self):
        return self.title
    
    def is_visible(self):
        if self.start_date and not self.start_date <= datetime.now():
            return False
        if self.end_date and self.end_date >= datetime.now():
            return False
        return True
    
    def get_collection_objects(self):
        object_set = []
        
        # Process and add appropriate breaking news items
        for obj in self.breakingnews_set.all():
            if obj.start_date and obj.end_date:
                if obj.start_date <= datetime.now() and obj.end_date >= datetime.now():
                    object_set.append(obj)
            elif obj.start_date:
                if obj.start_date <= datetime.now():
                    object_set.append(obj)
            elif obj.end_date:
                if obj.end_date >= datetime.now():
                    object_set.append(obj)
            else:
                object_set.append(obj)
        
        # Process and add appropriate collection items
        for obj in self.collectionitem_set.all():
            if obj.start_date and obj.end_date:
                if obj.start_date <= datetime.now() and obj.end_date >= datetime.now():
                    object_set.append(obj)
            elif obj.start_date:
                if obj.start_date <= datetime.now():
                    object_set.append(obj)
            elif obj.end_date:
                if obj.end_date >= datetime.now():
                    object_set.append(obj)
            else:
                object_set.append(obj)
        
        remainder = self.limit - len(object_set)
        if remainder > 0:
            # TODO Impliment behavior inline support instead of simple object insertion
            for obj in Story.objects.filter(categories=self.category).order_by('-pub_date')[:remainder]:
                append = True
                for item in self.breakingnews_set.all():
                    if obj == item.content_object:
                        append = False
                for item in self.collectionitem_set.all():
                    if obj == item.content_object:
                        append = False
                if append == True:
                    object_set.append(obj)
        return object_set

class BreakingNews(models.Model):
    collection = models.ForeignKey(Collection)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    start_date = models.DateTimeField(_('start date'), blank=True, null=True)
    end_date   = models.DateTimeField(_('end date'), blank=True, null=True)
    
    class Meta:
        verbose_name = _("breaking news item")
        verbose_name_plural = _("breaking news items")
        get_latest_by = 'start_date'
    
    def __unicode__(self):
        return u"%s" % self.content_object

class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    start_date = models.DateTimeField(_('start date'), blank=True, null=True)
    end_date   = models.DateTimeField(_('end date'), blank=True, null=True)
    
    class Meta:
        verbose_name = _("collection item")
        verbose_name_plural = _("collection items")
    
    def __unicode__(self):
        return u"%s" % self.content_object

ORDERING_CHOICES = (
    ('pub_date DESC', 'Publication date (Newest first)'),
    ('pub_date ASC', 'Publication date (Oldest first)'),
    ('COALESCE(update_date, pub_date) DESC', 'Update date (Newest first)'),
    ('COALESCE(update_date, pub_date) ASC', 'Update date (Oldest first)'),
    ('headline ASC', 'Headline (Alphabetical)'),
    ('headline DESC', 'Headline (Reverse alphabetical)'),
    ('RANDOM()', 'Random'),
)

class CollectionBehavior(models.Model):
    collection = models.ForeignKey(Collection)
    order_by = models.CharField(_('order by'), max_length=50, choices=ORDERING_CHOICES)
    
    class Meta:
        verbose_name = _("collection behavior")
        verbose_name_plural = _("collection behaviors")
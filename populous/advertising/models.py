from django.db import models
from django.core import exceptions
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from populous.advertising.parts.utils import get_admin_filter_ads

###############
##  Clients  ##
###############
class Client(models.Model):
    """
    A ``Client`` represent a company or an individual who has, or will in the future,
    run an ``Ad`` on one of our websites.
    """
    # Contact Info:
    name = models.CharField(_('business name'), max_length=200, blank=True)
    phone1 = models.CharField(_('primary phone number'), max_length=50, blank=True, null=True)
    phone2 = models.CharField(_('secondary phone number'),  max_length=50, blank=True, null=True)
    fax = models.CharField(_('fax number'), max_length=50, blank=True, null=True)
    email = models.EmailField(_('e-mail Address'), blank=True)
    website = models.URLField(_('website URL'), blank=True, null=True)
    
    # Address Info:
    address1 = models.CharField(_('street address 1'), max_length=200, blank=True)
    address2 = models.CharField(_('street address 2'), max_length=200, blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    state = models.CharField(_('state/province'), max_length=255, blank=True)
    zipcode = models.CharField(_('zipcode'), max_length=10, blank=True)
    country = models.CharField(_('country'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")
        app_label = 'advertising'
    
    def __unicode__(self):
        return self.name
    
    def get_client_ad_count(self):
        "Returns an ``int`` of the number of ads currently being run by this ``Client``."
        return self.client_ad_set.all().count()
    get_client_ad_count.short_description = 'number of ads'
    
    def get_client_ad_list(self):
        "Returns a ``list`` of all ads by this ``Client``."
        #TODO: fix this
        ad_types = ContentTypes.objects.filter(model__in=get_admin_filter_ads())
        ad_list = []
        for ad_type in ad_types:
            ads = ad_type.get_model_module().get_list(client__id__exact=self.id)
            if ads:
                ad_list.extend(ads)
        return ad_list

#################
##  Placement  ##
#################
PLACEMENT_TYPES = (
    (1, 'Single Ad'),
    (2, 'Multiple Ad'),
)

PLACEMENT_ORIENTATION = (
    (1, 'Vertical'),
    (2, 'Horizontal'),
)

class Placement(models.Model):
    """
    A ``Placement`` contains a mapping of ``Ad``\s to be displayed.  ``Placement``\s
    use a ``foreign_key``/``content_type`` pair to create a generic relationship
    """
    location = models.CharField(_('location'), max_length=255)
    notes = models.TextField(_('notes'), blank=True, null=True)
    type_placement = models.IntegerField(_('type'), choices=PLACEMENT_TYPES)
    sites = models.ManyToManyField(Site)
    
    num_ads = models.IntegerField(_('number of ads'), blank=True, null=True,
        help_text=_('Number of ads to display.  NOTE: this is only applicable to "Multi Ad" placements.'))
    template = models.CharField(max_length=255, blank=True, null=True)
    orientation = models.IntegerField(choices = PLACEMENT_ORIENTATION, default=1)
    
    image = models.ImageField(upload_to='img/advertisements/placements', blank=True, null=True)
    
    allowable_ad_types = models.ManyToManyField(ContentType, verbose_name=_('allowable ad types'),
        related_name="allowable_ad_types")  ## limit_choices_to={'model__in': get_admin_filter_ads()},
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    
    random = models.BooleanField(_('random'), default=False,
        help_text=_('If selected this placement will simply pull random ads from the selected list below.'))
    random_ad_types = models.ManyToManyField(ContentType, verbose_name=_('random ad type(s)'),
        related_name="random_ad_types", blank=True, null=True)  ## limit_choices_to={'model__in': get_admin_filter_ads()},
        
    def __unicode__(self):
        return self.location
    
    class Meta:
        app_label = 'advertising'
    
    def _get_default_template(self):
        """
        Returns a ``string`` representing a **relative** path to the default template.
        
        This uses the ``type_placement`` field of the ``Placement`` to determine the
        proper template. 
        """
        if self.type_placement == 1:
            return 'advertising/placements/placement_singlead_default'
        elif self.type_placement ==2 and self.orientation == 1:
            return 'advertising/placements/placement_multiad_default'
        elif self.type_placement ==2 and self.orientation == 2:
            # 'Horizontal' 'Multi Ad' Placement
            return 'advertising/placements/placement_multiadh_default'
        else:
            return None
        
    def get_ads(self, inc=False):
        """
        By default this method returns a ``list`` of ``Ad`` objects to be displayed.  It is basically
        an interpreter for ``type_placement``. Regardless of how many ads, this will **ALWAYS**
        return a list.
        
        Takes an optional ``True`` value which will return a list of (``ScheduledAd``, ``Ad``) tuples.
        """
        from custom.advertising.parts.utils import windex
        
        ad_list = []
        for scheduled_ad in self.scheduledad_set.filter(is_disabled__exact=False):
            ad_list.append((scheduled_ad, scheduled_ad.get_ad()))   # (ScheduledAd, Ad)
        
        if self.type_placement == 1:
            try:
                random_ad = windex([((ScheduledAd, Ad), ScheduledAd.priority) for ScheduledAd, Ad in ad_list])
                return [random_ad]
            except:
                return []
        else:
            #if inc:
            return ad_list
            #else:
            #    return [Ad for ScheduledAd, Ad in ad_list]
    
    
    def get_ad_count(self):
        """
        Returns an ``int`` of the number of ``ScheduledAd``\s currently scheduled
        to be displayed in this ``Placement``.
        """
        return len(self.get_ads())
    get_ad_count.short_description = "num running ads"
    
    def render(self, template=''):
        """
        This method returns a ``string`` which is the fully rendered representation
        of itself (a ``Placement``) and its ``Ad``\s (in HTML form).
        
        Accepts an optional ``template`` parameter which will override all other templates.
        """
        from django.template import loader, Context
        
        ad_list = []
        for ad in self.get_ads():
            ad_list.append({
                'ad': ad[1],
                'rendered_ad': ad[1].render(self, ad[0].template),
            })
        template = loader.select_template((
            'advertising/placements/' + template,
            'advertising/placements/' + self.template,
            self._get_default_template()
        ))
        context = Context({
            'ad_list': ad_list,
            'placement': self,
        })
        return template.render(context)

##################
##  Statistics  ##
###################
class Statistic(models.Model):
    """
    A ``Statistic`` is a fairly basic object which relates an ``Ad`` to a ``Placement``
    for a range of ``DateField``\s (``start_date`` and ``end_date``) as well as the number
    of clickthroughs and impressions during this date range.
    """
    ad_type = models.ForeignKey(ContentType, verbose_name=_('Ad type'))  ## limit_choices_to={'model__in': get_admin_filter_ads()}
    ad_id = models.PositiveIntegerField()
    
    placement = models.ForeignKey(Placement)
    
    clickthrough_count = models.PositiveIntegerField(default=0)
    impression_count = models.PositiveIntegerField(default=0)
    
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together = (('ad_type', 'ad_id', 'placement', 'start_date'),)
        app_label = 'advertising'
    
    def __unicode__(self):
        return u"%s (%s)" % (self.get_advertisement().name, self.get_advertisement().client)
    
    def get_advertisement(self):
        "Returns the ``Ad`` object."
        ad_type = self.ad_type
        return ad_type.get_object_for_this_type(pk=self.ad_id)
    get_advertisement.short_description = "advertisement"

#  Validators
def isExpiredAdvertisement(field_data, all_data):
    "A very simple validator that checks an ``Advertisement``\s ``is_expired`` field."
    if field_data:
        raise exceptions.ValidationError(_("This ad has expired.  To <strong>rerun</strong> this ad click 'save as new' above."))


#####################
##  Scheduled Ads  ##
#####################

PRIORITY_LEVELS = (
    (.1, 'default'),
    (.2, 2),
    (.4, 3),
    (.8, 4),
)

BEHAVIOR_TYPES = (
    (0, 'Basic'),
    (1, 'Date'),
    (2, 'Impression'),
    (3, 'Click-through'),
)

class ScheduledAd(models.Model):
    """
    A ``ScheduledAd`` is an ``edit_inline`` object to the ``Placement`` class.  This class is basically
    an ``Ad`` object with extra *display-related* fields.
    """
    placement = models.ForeignKey(Placement)
    
    ad_type = models.ForeignKey(ContentType, verbose_name=_('ad type'))  ## limit_choices_to={'model__in': get_admin_filter_ads()}
    ad_id = models.PositiveIntegerField(_('ad id'))
    
    notes = models.TextField(_('notes'), blank=True, null=True)
    
    is_disabled = models.BooleanField(_('disable ad'), default=False,
        help_text=_('''If checked than this ad <strong>will not</strong> display in this placement.'''))
    start_date = models.DateTimeField(_('start date'),
        help_text=_('''<strong>Date and time ad goes live</strong>.  If you do not add a date, the ad will go live <strong>immediatley</strong>.'''))
    
    priority = models.DecimalField(choices=PRIORITY_LEVELS, default=.1, max_digits=2, decimal_places=1,
        help_text=_('''
            Each number <strong>doubles</strong> the probability of showing the ad over the previous number.
            For example, an ad with priority 2 will show up <strong>twice</strong> as often as an ad with the default priority.'''))
    behavior = models.PositiveIntegerField(max_length=5, choices=BEHAVIOR_TYPES, default=0,
        help_text=_('''
            <strong>Basic</strong>: A <em>basic</em> ad will run until manually stopped.<br />
            <strong>Date</strong>: A <em>date</em> ad will run until the specified date.<br />
            <strong>Impression</strong>: An <em>impression</em> ad will run until the specified number of impressions has been reached.<br />
            <strong>Click-through</strong>: A <em>click-through</em> ad will run until the specified number of click-throughs has been reached.<br />
        '''))
    impression_limit = models.PositiveIntegerField(_('impressions'), blank=True, null=True)
    clickthrough_limit = models.PositiveIntegerField(_('click-throughs'), blank=True, null=True)
    
    
    end_date = models.DateTimeField(_('end date'), blank=True, null=True,
        help_text=_('''<strong>Date and time ad expires</strong>.'''))
    
    template = models.CharField(_('template'), max_length=255, blank=True, null=True)
    
    stat_id = models.IntegerField(editable=False, blank=True, null=True)
    is_expired = models.BooleanField(default=False, editable=False)
    
    class Meta:
        order_with_respect_to = 'placement'
        app_label = 'advertising'
    
    def __unicode__(self):
        return u"%s" % (self.get_ad())
    
    def _create_statistic(self):
        """
        Returns ``True`` if a ``Statistic`` was created, ``False`` otherwise.
        
        This shouldn't ever need to be called manually as it is called by this
        object's ``save()`` method.
        """
        #   Create Statistic object
        if not self.stat_id:
            stat = Statistic(
                ad_type_id = self.ad_type_id,
                ad_id = self.ad_id,
                placement = self.placement
            )
            stat.save()
            self.stat_id = stat.id
            self.save()
            
            return True
        return False
    
    def save(self):
        super(ScheduledAd, self).save()
        self._create_statistic()
    
    def get_ad(self):
        """
        Returns the proper ``Ad`` object.
        """
        return self.ad_type.get_model_module().get_object(pk=self.ad_id)


###############
##  Coupons  ##
###############

ORIENTATION_CHOICES = (
    ('V', 'Vertical'),
    ('L', 'Landscape'),
)

class CouponCategory(models.Model):
    """
    A ``CouponCategory`` is a simple model to help logically group
    ``Coupon`` instances to a commmon category.
    """
    
    name = models.CharField(_('name'), max_length=200, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    
    class Meta:
#        app_label = 'advertisements'
        verbose_name_plural=_("coupon categories")
    
    def __unicode__(self):
        return self.name

################################
##  Base Advertisement Model  ##
################################
class BaseAd(models.Model):
    """
    Base advertisement model.
    
    Do not use this directly as it isn't functional by itself.  All ``Ad``
    instances need to extend this model.
    """
    
    #name = models.CharField(max_length=255)
    #slug = models.SlugField(prepopulate_from=["name"], unique=True)
    #client = models.ForeignKey(Client, raw_id_admin=True)
    
    def get_module_name(self):
        return self._meta.module_name
        
    def get_app_name(self):
        return self._meta.app_label
    
    def get_meta_info(self, type):
        try:
            return eval('self._meta.%s' % type)
        except:
            return None
    
    def get_size(self):
        """
        Returns the 'size' of the ad.  Every ad should extend this function to return the size of the ad.
        This function is used by Placements 
        """
    
    def __unicode__(self):
        return u"%s | %s" % (self.client or self.one_off_client or "None", self.name)
    
    def stat_list_lookup(self, placement=None):
        """
        If no Placement is passed, then a list of all Statistic objects related to this ad are returned.
        If a Placement is passed, then the single matching Statistic object will be returned.
        Regardless of how this is called, a tuple or a None type is returned.
        """
        from populous.advertising.models.base import statistics as adstats
        from django.contrib.contenttypes.models import ContentType
        ad_type = ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.module_name)
        if not placement:
            try:
                return adstats.objects.filter(ad_type__id__exact=ad_type.id, ad_id__exact=self.id)
            except:
                return None
        else:
            try:
                placement_type = ContentType.objects.get(app_label=self._meta.app_label, model=self._meta.module_name)
                return (adstats.objects.get(ad_type__id__exact=ad_type.id, ad_id__exact=self.id, placement__id__exact=placement.id), )
            except:
                return None
            
    def get_impression_count(self, placement=None):
        """Returns the number of impressions for this ad over ALL placements on ALL sites."""
        stats = self.stat_list_lookup(placement)
        total = 0
        for stat in stats:
            total += stat.impression_count
        return total
    
    def get_clickthrough_count(self, placement=None):
        """Returns the number of clickthroughs for this ad over ALL placements on ALL sites."""
        stats = self.stat_list_lookup(placement)
        total = 0
        for stat in stats:
            total += stat.clickthrough_count
        return total
    
    def add_impression(self, placement):
        """
        Increments the ``impression_count`` for this ``Ad`` and ``Placement``.
        
        Requires a ``Placement`` object to be passed in.
        """
        stat = self.stat_list_lookup(placement)[0]
        stat.impression_count += 1
        stat.save()
    
    def add_clickthrough(self, placement):
        """
        Increments the ``clickthrough_count`` for this ``Ad`` and ``Placement``.
        
        Requires a ``Placement`` object to be passed in.
        """
        stat = self.stat_list_lookup(placement)[0]
        stat.clickthrough_count += 1
        stat.save()
    
    def get_absolute_url(self):
        """Implement this in each Advertisement model to return the proper URL."""
        return ''
        
    def get_ad_url(self):
        """
        ALWAYS CALL THIS FROM THE TEMPLATES BECAUSE IT TRACKS CLICKTHROUGHS!
        
        Did you catch all that??
        """
        return '/advertising/click?ad=%s&ct=%s' % (self.id, self._meta.get_content_type_id())
    
    def render(self, placement, template=''):
        """
        Each ``Ad`` should know how to render itself.
        """
        from django.template.loader import select_template
        from django.template import Context
        
        self.add_impression(placement)
        
        default_template = "advertising/advertisements/%s_default" % self._meta.module_name
        template = select_template(('advertising/advertisements/%s' % template, default_template,))
        c = Context({
            'ad': self,
            'placement': placement,
        })
        return template.render(c)

###################################
###################################
#   Specific Advertising Models  ##
###################################
###################################
class TextAd(BaseAd):
    """
    A ``TextAd`` is the most basic ``Ad``.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))
    kicker = models.CharField(max_length=200, blank=True, 
        help_text=_('''
            This text will be displayed as a link to the text ad's details.<br />
            <strong>NOTE</strong>: If there is no kicker, then the add will assume that it is only supposed to display the graphic and address information.'''))
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    decked_head = models.CharField(_('decked head'), max_length=200, blank=True)
    content = models.TextField(_('content'), max_length=2000, blank=True)
    
    image = models.ImageField(_('image to upload'), upload_to='img/advertisements/text_ads/%Y/%m/%d', blank=True, null=True)
    image_only = models.BooleanField(help_text=_('''Choose this if you only want this ad to be represented as an <strong>image only</strong>.'''))
    
    link = models.URLField(blank=True, null=True)
    link_only = models.BooleanField(default=False, help_text=_('''Choose this if you only want this ad to be represented as an <strong>link only</strong>.'''))
    
    ADMIN_FILTER_DISPLAY = True
    
#    class Meta:
#        app_label = 'advertisements'
    
    def get_absolute_url(self):
        return self.link or None

class GraphicAd(BaseAd):
    """
    A ``GraphicAd`` is simply an image and an optional url.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))
    image = models.ImageField(_('Image to Upload'), upload_to='img/ads/graphic/%Y/%m/%d')
    url = models.URLField(_('url'), blank=True, help_text=_('''If you want the ad to be clickable, enter the url here.'''))
    
    ADMIN_FILTER_DISPLAY = True
    
#    class Meta:
#        app_label = 'advertisements'
    
    def get_absolute_url(self):
        return self.url or None

class VideoAd(BaseAd):
    """
    A ``VideoAd`` is similar to a ``GraphicAd``, but displays a video instead of
    an image.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))
    video = models.FileField(upload_to='videos/advertisements/%Y/%m/%d')
    url = models.URLField(_('url'), blank=True)
    
    ADMIN_FILTER_DISPLAY = True
    
#    class Meta:
#        app_label = 'advertisements'

class Coupon(BaseAd):
    '''
    Exactly what it sounds like.  The only additional thing is that there is an
    image orientation field that prompts a friendly reminder to change your page
    settings for your printer to landscape for best results.
    
    A `Coupon` belongs in a ``CouponCategory``.
    '''
    
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True)
    client = models.ForeignKey(Client, verbose_name=_('client'))
    headline = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(CouponCategory)
    image = models.ImageField(upload_to='img/advertisements/coupons/%Y/%m/%d')
    image_orientation = models.CharField(_('Image Orientation'), max_length=1, choices=ORIENTATION_CHOICES)
    
    ADMIN_FILTER_DISPLAY = True
    
#    class Meta:
#        app_label = 'advertisements'

# Classifieds

class ClassifiedSubCategory(models.Model):
    """		Child of ClassifiedsCategory, parent of ClassifiedsAd."""
    name = models.CharField(max_length=200, unique=True)
    sub_category_id = models.IntegerField(unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Classifieds Sub-Categories"
        ordering = ['sub_category_id']
    
    def __unicode__(self):
        return '%s %s' % (self.sub_category_id, self.name)

class ClassifiedCategory(models.Model):
    """		Top Classified parent."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    sub_categories = models.ManyToManyField(ClassifiedSubCategory)
    
    class Meta:
        verbose_name_plural = "Classifieds Categories"
        ordering = ['name']
    
    def __unicode__(self):
        return self.name

class ClassifiedAd(models.Model):
    """		Simple classified with optional address information."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    live_date = models.DateTimeField('Date Added')
    subcategory = models.ForeignKey(ClassifiedSubCategory)
    ad_id = models.IntegerField(unique=True)
    content = models.TextField()
    auto_imported = models.BooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Classifieds Ads"
    
    def __unicode__(self):
        return self.name

class UploadClassifiedAdSet(models.Model):
    date = models.DateTimeField(_('Ad Set for Date'))
    file = models.FileField(upload_to="classifieds/")
    
    def __unicode__(self):
        return self.file
    
class CurrentClassifiedAdSet(models.Model):
    name = models.CharField(max_length=1000)
    file = models.FilePathField(path="classifieds/")
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        super(CurrentClassifiedAdSet, self).save()
        from datetime import datetime
        from django.template.defaultfilters import slugify
        from django.core.exceptions import ObjectDoesNotExist
        from populous.advertising.parts.parser import xml_parser
        sections = xml_parser(self.file)
        
        for file in UploadClassifiedAdSet.objects.all().order_by('-date')[3:]:
            file.delete()
        
        for ad in ClassifiedAd.objects.filter(auto_imported=True):
            ad.delete()
        
        for section in sections:
            try:
                current_section=ClassifiedSubCategory.objects.get(sub_category_id=int(section.callnumber))
            except:
                ClassifiedSubCategory.objects.create(name=section.name, sub_category_id=int(section.callnumber), slug=slugify(section.name)).save()
                current_section=ClassifiedSubCategory.objects.get(sub_category_id=int(section.callnumber))
            for ad in section.ads:
                # Check for pre-existing Ad
                try:
                    ClassifiedAd.objects.get(ad_id=int(ad.id))
                    continue
                except:
                    pass
                
                # Create new auto_imported Ad
                newAd=ClassifiedAd.objects.create(
                    name=ad.name,
                    slug="%s%s" % (ad.name[:25], str(ad.id)),
                    ad_id=int(ad.id),
                    live_date=datetime.now(),
                    subcategory=current_section,
                    content=ad.text,
                    auto_imported = True
                )
                newAd.save()

#        
#        from django.models.advertising import classifiedads
#        from django.core.template import Context, Template
#        
#        ## Open Files
#        OUTPUT = open('/home/html/templates/dailybruin.com/ssi/classified_ads_top6.html', 'wb')
#        TEMPLATE = Template(open('/home/html/templates/dailybruin.com/ssi/classified_ads_top6_template.html', 'r').read())
#        
#        ## Top 6 Calssified Ads
#        ad_list=[]
#        ad_list=classifiedads.get_list(order_by=['?'], limit=6)
#        ad_list_context = Context({'ad_list': ad_list})
#        
#        ## Save the Output to File
#        OUTPUT.write(TEMPLATE.render(ad_list_context))
#        OUTPUT.close()
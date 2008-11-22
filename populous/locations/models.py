from django.db import models
from django.utils.translation import ugettext_lazy as _

TIME_ZONE_OFFSETS = (
    (0, '-1200'),
    (1, '-1100'),
    (2, '-1000'),
    (3, '-0900'),
    (4, '-0800'),
    (5, '-0700'),
    (6, '-0600'),
    (7, '-0500'),
    (8, '-0400'),
    (9, '-0300'),
    (10, '-0200'),
    (11, '-0100'),
    (12, '+0000'),
    (13, '+0100'),
    (14, '+0200'),
    (15, '+0300'),
    (16, '+0400'),
    (17, '+0500'),
    (18, '+0600'),
    (19, '+0700'),
    (20, '+0800'),
    (21, '+0900'),
    (22, '+1000'),
    (23, '+1100'),
    (24, '+1200'),
)

class LocationType(models.Model):
    """
    A ``LocationType`` represent a type of ``Location`` object.  This is used to help
    group similar ``Location`` objects into some sort of category, but it is also used to
    _intelligently_ display ``Location`` objects names (including thier ``parent`` objects).
    """
    name = models.CharField(_('name'), max_length=255, unique=True)
    name_plural = models.CharField(_('plural name'), max_length=255, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    slug = models.SlugField(_('slug'), unique=True)
    
    class Meta:
        verbose_name = _('location type')
        verbose_name_plural = _('location types')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

class LocationManager(models.Manager):
    def type(self, type, **kwargs):
        """
        Convienience method to access particular ``Location`` objects of a certain ``LocationType``.
        
        Usage:
            Location.objects.type('city', name='San Francisco') # Returns a ``Location`` queryset
        """
        return super(LocationManager, self).get_query_set().filter(location_type__name__iexact=type, **kwargs)

class Location(models.Model):
    """
    Describes ANY location on Earth.  Very flexible and custom managers allows for convienient
    access to common types of locations (such as countries, states, cities, etc).
    """
    # Basic Information
    name = models.CharField(_('name'), max_length=255)
    display_name = models.CharField(_('display name'), max_length=255, blank=True, null=True,
        help_text=_("ex: Home, Work, School..."))
    abbreviation = models.CharField(_('abbreviation'), max_length=100, blank=True, null=True,
        help_text=_("If this is a Country, you MUST use the country-code here."))
    use_abbreviation = models.BooleanField(_('use abbreviation instead of name as default.'), default=False)
    
    # Address Information
    address1 = models.CharField(_('address1'), max_length=500, blank=True, null=True)
    address2 = models.CharField(_('address2'), max_length=500, blank=True, null=True)
    postal_code = models.CharField(_('zip code'), max_length=20, blank=True, null=True)
    
    # Extended Information
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField(_('description'), blank=True)
    timezone = models.IntegerField(_('timezone'), choices=TIME_ZONE_OFFSETS, blank=True, null=True)

    # Geogrpahic Information
    latitude = models.DecimalField(_('latitude'), max_digits=11, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(_('longitude'), max_digits=11, decimal_places=6, blank=True, null=True)

    # Relational Information
    location_type = models.ForeignKey(LocationType, verbose_name=_('type'),
        help_text=_("examples: City, State, Country..."))
    parent = models.ForeignKey('self', blank=True, null=True, related_name="child", verbose_name=_('parent'), parent_link=True,
        help_text=_("If this location is a more specific location which belongs to a larger location (such as a city in a state), you can select the 'parent' location here."))
    default_for_type = models.BooleanField(_('default location'), default=False)  #TODO: Make this ENFORCED!
    
    slug = models.SlugField(_('slug'))

    internal_name = models.CharField(_('location relation'), max_length=255, blank=True)
    
    objects = LocationManager()
    
    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ('name',)
        unique_together = (('slug', 'parent', 'location_type'),)
    
    def __unicode__(self):
        return u"%s: %s" % (self.location_type, self.name)
    
    def get_parent_type(self, location_type):
        """
        This method will return the _first_ parent ``Location`` that matches ``location_type``.
        
        Example:
            >>> la = Location.objects.get(slug='los_angeles')
            >>> la.get_parent_type('state')
            state: California
        """
        parent = self.parent
        while parent:
            if parent.location_type.name == location_type:
                return parent
            parent = parent.parent
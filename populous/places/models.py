from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from populous.locations.models import Location
from populous.places.query import PlaceOptionQuerySet

PLACE_OPTION_CHOICES = (
    (0, 'check box'),
    (1, 'input field'),
)

class OptionManager(models.Manager):    
    #def __init__(self):
        #super(OptionManager, self).__init__()
        #self.query._option_extra = False
    
    def _clone(self, klass=None, setup=False, **kwargs):
        c = super(OptionManager, self)._clone(klass, setup, **kwargs)
        c._get_base_query = self._get_base_query
        c._build_query = self._build_query
        return c
        
    def _get_base_query(self, value):
        query = '''
            SELECT "places_inlineplaceoption"."object_id" 
            FROM "places_inlineplaceoption", "places_placeoption"
            WHERE "places_inlineplaceoption"."place_option_id" = "places_placeoption"."id"
            AND "places_placeoption"."arg_name" = %s
        '''

        if value is True or value is False:
            query += 'AND "places_inlineplaceoption"."bool" = %s'
        else:
            query += 'AND "places_inlineplaceoption"."value" = %s'
        return query
    
    def _build_query(self, **kwargs):
        from django.db import connection
        cursor = connection.cursor()
        
        query, queries = '', []
        params = list(kwargs.items()[0])
        
        for arg_name, value in kwargs.items()[1:]:
            q = '\nAND "places_inlineplaceoption"."object_id" IN (' + self._get_base_query(value)
            queries.append(q)
            params.extend([arg_name, value])
        
        query = '\n'.join(queries)
        for q in queries:
            query += ')'
        
        query = self._get_base_query(params[1]) + query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [i[0] for i in rows]
    
    def filter(self, *args, **kwargs):
        """
        This overrides the default ``filter`` method and adds the ability
        to lookup a place by ``PlaceOption`` using the same syntax that is
        used in a normal queryset lookup.
        
        Take the folowing example.  We want to return all ``Restaurant``
        objects that have a custom ``PlaceOption`` called ``accepts_bruincard``.
        We can do this like so::
        
            >>> Restaurant.objects.filter(accepts_bruincard=True)
            [<Restaurant: Bombay Bite>, <Restaurant: Starbucks>]
        
        Additionally, if we wanted to find all ``Restaurant``s that are open late,
        and have an associated ``PlaceOption`` called ``open_late``, we can do the
        following::
        
            Restaurant.objects.filter(accepts_bruincard=True, open_late=True)
            [<Restaurant: Starbucks>]
        
        
        NOTE: As of right now, this *only* supports ``exact`` lookups.
        """
        from django.core.exceptions import FieldError
        failed_kwargs = {}
        qs = super(OptionManager, self).filter(*args)
        for key, value in kwargs.items():            
            try:
                qs = qs.filter(**{key: value})
            except FieldError, e:
                # Failed lookup for keyword, so try PlaceOption
                failed_kwargs[key] = value
        id_list = self._build_query(**failed_kwargs)
        if id_list:
            return qs.filter(pk__in=id_list)
        else:
            # If id_list is None, then nothing matched
            return qs.none()

class PlaceOption(models.Model):
    #TODO: Change the name of this
    name = models.CharField(max_length=500)
    arg_name = models.CharField(max_length=500, unique=True,
        help_text=_('This should be a valid python argument name (e.g, spaces should be underscores and no other punctiation should be used)'))
    type = models.IntegerField(choices = PLACE_OPTION_CHOICES)
    
    def __unicode__(self):
        return self.name

class InlinePlaceOption(models.Model):
    place_option = models.ForeignKey(PlaceOption)
    
    bool = models.BooleanField(_('value'), default=False)
    value = models.CharField(_('value'), max_length=500, blank=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    place_type = generic.GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = (('place_option', 'content_type', 'object_id'),)
        verbose_name = 'Extended Option'
    
    def __unicode__(self):
        return self.place_option.get_type_display()
    
    def option_type(self):
        return self.place_option.type

def get_school_choices():
    Q = models.Q
    return Q(location_type__slug='schools')

#///////////////////////////////////////////////////////
#       School
#///////////////////////////////////////////////////////
class School(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    location = models.ForeignKey(Location, verbose_name=_('location'))  #limit_choices_to=get_school_choices()
    abbreviation = models.CharField(_('abbreviation'), max_length=50, blank=True, null=True)
    mascot = models.CharField(_('mascot'), max_length=200, blank=True, null=True)
    mascot_plural = models.CharField(_('mascot, plural form'), max_length=200, blank=True, null=True,
        help_text=_("Ex: For UCLA Bruins, you would enter Bruins in this field"))
    logo = models.ImageField(_('logo'), upload_to='img/sports/logos', blank=True, null=True,
        help_text=_("Images must be one of the following formats: jpg|jpeg|gif|png|"))

    class Meta:
        ordering = ('name',)
        verbose_name = _('School')
        verbose_name_plural = _('Schools')

    def __unicode__(self):
        return self.name
    
    def get_display_name(self):
        try: return self.abbreviation
        except: return self.name
    
    def get_matches(self, location=None):
        """
        This provides easy access to a queryset of ``Match`` objects representing matches played
        by this team.  ``location`` can be ``home``, ``away`` or ``None`` (not passed).

        Requires:
            populous.sports
        """
        try:
            from populous.sports.models import Match
        except:
            raise NotImplementedError, "populous.sports is not installed."
            kwargs = {}
        if location is 'home' or location is 'away':
            kwargs[location + '_team__name'] = self.name
        return Match.objects.filter(**kwargs)

#///////////////////////////////////////////////////////
#       Restaurant
#///////////////////////////////////////////////////////
class Cuisine(models.Model):
    name = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u'/restaurants/cuisine/%s' % self.id

class Restaurant(models.Model):
    name = models.CharField(max_length=500)
    location = models.ForeignKey(Location)  #limit_choices_to=models.Q(location_type__slug='restaurants') WHY DOESN'T THIS WORK??
    price_low = models.PositiveSmallIntegerField('price (low)', blank=True, null=True)
    price_high = models.PositiveSmallIntegerField('price (high)', blank=True, null=True)
    local = models.NullBooleanField('locally owned')
    outdoor_seating = models.NullBooleanField('outdoor seating available')

    pay_visa = models.NullBooleanField('Visa')
    pay_mastercard = models.NullBooleanField('MasterCard')
    pay_discover = models.NullBooleanField('Discover')
    pay_amex = models.NullBooleanField('American Express')
    pay_checks = models.NullBooleanField('checks')

    accept_reservations = models.NullBooleanField('accepts reservations')
    accept_callaheads = models.NullBooleanField('accepts call-aheads')

    kids_menu = models.NullBooleanField()
    party_room = models.NullBooleanField('party room (20+)')
    live_music = models.NullBooleanField('occasional live music')

    num_vegetarian = models.PositiveSmallIntegerField('# of vegetarian dishes', blank=True, null=True)
    num_vegan = models.PositiveSmallIntegerField('# of vegan dishes', blank=True, null=True)
    num_tvs = models.PositiveSmallIntegerField('# of TVs', blank=True, null=True)

    ed_pick = models.NullBooleanField('editor pick')
    has_delivery = models.NullBooleanField('has delivery')
    has_buffet = models.NullBooleanField('has buffet')
    icon = models.ImageField(blank=True, upload_to='img/places/icons')
    featured_date = models.DateField(blank=True, null=True, help_text="The date on which this restaurant was Featured Restaurant.")
    cuisines = models.ManyToManyField(Cuisine)
    
    disable_comments=models.BooleanField("click to disable comments for this restaurant.", blank=True, null=True)
    
    inlineplaceoption_set = generic.GenericRelation(InlinePlaceOption)
    
    objects = OptionManager()
    
    
    def __unicode__(self):
        return self.location.name

    #TODO: Add get_absolute_url
    
    def options(self):
        """
        This method returns a ``dictionary`` mapping of ``PlaceOption`` objects
        to their respective values for the given model.
        """
        if not hasattr(self, "_options_cache"):
            opt_dict = {}
            for opt in self.inlineplaceoption_set.all():
                if opt.place_option.type == 0:
                    # This is a boolean
                    opt_dict[opt.place_option.name] = opt.bool
                else:
                    # This is a value
                    opt_dict[opt.place_option.name] = opt.value
            self._options_cache = opt_dict
        return self._options_cache
    
    def get_price(self):
        "Returns this restaurants's price as a pretty formatted string such as '$3 - $5'"
        if self.price_low == self.price_high == 0:
            return u'Free'
        if self.price_low == self.price_high == None:
            return u''
        if self.price_low == self.price_high:
            price = u'$%.2f' % self.price_low
        elif self.price_low == 0:
            price = u'Free - $%.2f' % self.price_high
        elif self.price_high == 0:
            price = u'$%.2f' % self.price_low
        else:
            price = u'$%.2f - $%.2f' % (self.price_low, self.price_high)
        return price.replace('.00', '')
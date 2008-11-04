from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from populous.places.models import School
#from django.conf import settings

# The name of the default team
DEFAULT_SCHOOL = 'University of California Los Angeles' #TODO: move this into settings

GENDER_CHOICES = (
    ('M', _('Men')),
    ('W', _('Women')),
)

class Sport(models.Model):
    name = models.CharField(_('sport'), max_length=200, unique=True)
    slug = models.SlugField(_('slug'), unique=True)
    
    class Meta:
        verbose_name = _('sport')
        verbose_name_plural = _('sports')
    
    def __unicode__(self):
        return self.name

class MatchManager(models.Manager):
    _("""
    Special ``Manager`` for ``Match`` objects which allows for easy retrieval of ``Match``es
    for a ``School``.
    
    Usage:
    
    # Get a queryset of all matches in which UCLA played.
    Match.objects.school(abbreviation="UCLA")
    
    # Get a queryset of all basketball matches in which Stanford played.
    Match.objects.school(name="Stanford").filter(sport__name="Basketball")
    """)
    def school(self, **kwargs):
        if kwargs.get('name'):
            school = kwargs.get('name')
            return super(MatchManager, self).get_query_set().filter(
                models.Q(home_team__name=school) | models.Q(away_team__name=school) )
        elif kwargs.get('abbreviation'):
            school = kwargs.get('abbreviation')
            return super(MatchManager, self).get_query_set().filter(
                models.Q(home_team__abbreviation=school) | models.Q(away_team__abbreviation=school) )
        else:
            return self.none()

class Match(models.Model):
    sport = models.ForeignKey(Sport)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES)
    game_time = models.DateTimeField(_('game time'))
    
    home_team = models.ForeignKey(School, related_name="home_team", verbose_name=_('home team'))
    away_team = models.ForeignKey(School, related_name="away_team", verbose_name=_('away team'))
    home_team_score = models.FloatField(_('home team score'), blank=True)   #TODO: this should probably be a DecimalField
    away_team_score = models.FloatField(_('away team score'), blank=True)

    class Meta:
        ordering = ('game_time',)
        verbose_name = _('match')
        verbose_name_plural = _('matches')

    def __unicode__(self):
        return _("%s's %s: %s(%d) vs. %s(%d) - %s") % (
            self.get_gender_display(),
            self.sport,
            self.home_team.get_display_name(),
            self.home_team_score,
            self.away_team.get_display_name(),
            self.away_team_score,
            self.game_time)
    
    objects = MatchManager()

class SportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}

class MatchAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Match Details'),
            {'fields': (('sport','gender'), 'game_time')
        }),
        (_('Scores'),
            {'fields': (('home_team', 'home_team_score'), ('away_team', 'away_team_score'))
        }),
    )
    list_filter = ('gender',)

admin.site.register(Sport, SportAdmin)
admin.site.register(Match, MatchAdmin)
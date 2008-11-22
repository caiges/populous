from django import template
from django.conf import settings
from populous.sports.models import Score
from populous.core.templatetags import CachedNode
from django.utils.translation import ugettext_lazy as _

register = template.Library()

class RecentScoresNode(CachedNode):
    def __init__(self, num, sport, gender):
        self.num = num
        self.sport = sport
        self.gender = gender

    def __str__(self):
        return "<RecentScoresNode>"

    def get_cache_key(self, context):
        return "populous.sorts.templatetags.sports:%s:%s:%s:%s" % (settings.SITE_ID, self.num, self.sport, self.gender)

    def get_content(self, context):
        if self.sport:
            scores_list = Score.objects.filter(sport__name=self.sport)[:self.num]
        else:
            scores_list = Score.objects.all()[:self.number]
        try:
            score_set = ''
            for game in scores_list:
                score_set += '''<div class="sports">\n
                    <p><span class="sport">%s's %s</span> <span class="competitors">UCLA vs. %s</p>\n
                    <p>UCLA: %s</p>
                    <p>%s: %s</p>
                </div>''' % (game.get_gender_display(), game.get_sport(), game.get_opponent().abbreviation, game.score_ucla, game.get_opponent().abbreviation, game.score_rival)
            return score_set
        except:
            return _('<!-- Error: No sport scores could be retrieved -->')

def do_scores(parser, token):
    """
    Usage:
    {% get_sport_scores [num scores] [sport] [gender] %}
    
    ``sport`` and ``gender`` are optional.
    
    examples:
        Get the 5 latest ``soccer`` scores:
        >>> {% get_sport_scores 5 soccer %}
        
        Get the 10 latest ``women``s scores:
        >>> {% get_sport_scores 10 women %}
        
        Get the latest ``men``s ``football`` score:
        >>> {% get_sport_scores 1 football men %}
        
    """
    bits = token.contents.split()
    if len(bits) == 2:
        return RecentScoresNode(bits[1], None, None)    # No filter
    elif len(bits) == 3:
        if bits[2].lower() in [v.lower() for k, v in GENDER_CHOICES]:
            return RecentScoresNode(bits[1], None, bits[2]) # Gender filter only
        else:
            return RecentScoresNode(bits[1], bits[2], None)   # Sport filter only
    elif len(bits) == 4:
        if not bits[3].lower() in [v.lower() for k, v in GENDER_CHOICES]:
            raise template.TemplateSyntaxError, _("'%s' tag requires the last argument to be a valid gender.") % bits[0]
        else:
            return RecentScoresNode(bits[1], bits[2], bits[3])  # Sport and gender filter
    else:
        raise template.TemplateSyntaxError, _("'%s' tag takes 1 or 2 arguments, an integer value for the number of score sets to return and otionally a sport.") % bits[0]

register.tag('get_sport_scores', do_scores)
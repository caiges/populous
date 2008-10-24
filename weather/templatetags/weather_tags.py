from django import template
from weather.models import Forecast, ForecastDay

register = template.Library()

class LatestForecastNode(template.Node):
    
    def __init__(self, varname='latest_forecast'):
        self.varname = varname
    
    def render(self, context):
        context[self.varname] = Forecast.objects.latest_with_icon()
        return ''
        

@register.tag
def get_latest_with_icon(parser, token):
    """
    {% get_latest_with_icon [as latest_forecast]  %}
    
    Returns the last Forecast that has an icon attached.
    Each forecast updated hourly has an icon, where as the ones
    updated more often don't have icon data.
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return LatestForecastNode()
    elif len(bits) == 3:
        return LatestForecastNode(bits[2])
    else:
        raise template.TemplateSyntaxError("%s: Argument takes 0 or 2 arguments" % bits[0])


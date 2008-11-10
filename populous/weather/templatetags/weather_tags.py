from django import template
from weather.models import Forecast, ForecastDay

from datetime import datetime

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


class ForecastDayNode(template.Node):
    
    def __init__(self, num_days=1, varname='forecast_list'):
        self.num_days = int(num_days)
        self.varname = varname
    
    def render(self, context):
        context[self.varname] = ForecastDay.objects.filter(forecast_date__gte=datetime.now()).order_by('forecast_date')[:self.num_days]
        return ''

@register.tag
def get_forecast_list(parser, token):
    """
    {% get_forecast_list [num_days] [as latest_forecast]  %}
    
    Returns the ``num_days`` ForecastDay objects.
    """
    bits = token.split_contents()
    if bits[2] == 'as' and len(bits) == 4:
        return ForecastDayNode(bits[1], bits[3])
    elif len(bits) == 2:
        return ForecastDayNode(bits[1])
    elif len(bits) == 1:
        return ForecastDayNode()
    else:
        raise template.TemplateSyntaxError("%s: Argument takes either 0, 1 or 3 arguments." % bits[0])
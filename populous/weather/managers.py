from django.db.models import Manager
import datetime

class ForecastDayManager(Manager):
    """This adds some methods to the ForecastDay objects manager"""
    def __init__(self, *args, **kwargs):
        super(ForecastDayManager, self).__init__(*args, **kwargs)
    
    def get_latest(self, num, no_sun_data=True):
        return self.get_query_set().all().filter(sun_set__isnull=no_sun_data)[:num]

class ForecastManager(Manager):
    """This adds some methods to the ForecastDay objects manager"""
    def __init__(self, *args, **kwargs):
        super(ForecastManager, self).__init__(*args, **kwargs)
    
    def get_latest(self, num):
        return self.get_query_set().all()[:num]
    
    def latest_with_icon(self):
        return self.get_query_set().filter(icon__isnull=False)[0]
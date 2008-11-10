from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from weather.managers import ForecastManager, ForecastDayManager

#The latest one of these will be your 'current'
class Forecast(models.Model):
    """
    Holds your latest forecast and all the forecasts for
    previous dates and 'checkins' 
    """
    observation_time = models.DateTimeField(unique=True)
    location = models.CharField(max_length=50)
    human_location = models.CharField(max_length=50, blank=True, null=True)
    temperature = models.FloatField()
    humidity = models.IntegerField(max_length=4)
    wind_speed = models.FloatField(max_length=6)
    wind_direction = models.CharField(max_length=5)
    icon = models.CharField(max_length=50, blank=True, null=True)
    conditions = models.CharField(max_length=50) 
    
    objects = ForecastManager()
    
    class Meta:
        ordering = ['-observation_time']
        get_latest_by = 'observation_time'
        
    def get_absolute_url(self):
        date = self.observation_time
        return reverse('forecast_detail', None, (), {
                'year': date.year,
                'month': date.strftime('%b').lower(),
                'day': date.day,
                'object_id': self.id,
                })
    
    def __unicode__(self):
        return "%s at %s" % (self.location, self.observation_time)
    
    def sun_or_moon(self):
        HALF_PERIOD = 14.5
        latest_data = ForecastDay.objects.get_latest(1, False)[0]
        result = "%s" % self.icon
        if (latest_data.sun_set <= datetime.now() and datetime.now().hour > 12) or (datetime.now().hour < 12 and latest_data.sun_rise >= datetime.now()):
            result += '_moon'
            illumination = int(latest_data.moon_illuminated)
            if illumination < 12.5:
                result += '_new'
            elif illumination >= 12.5 and illumination < 38:
                if latest_data.moon_age < HALF_PERIOD:
                    result += '_waxing_crescent'
                else:
                    result += '_waning_crescent'
            elif illumination >= 38 and illumination < 63:
                if latest_data.moon_age < HALF_PERIOD:
                    result += '_first_quarter'
                else:
                    result += '_last_quarter'
            elif illumination >= 63 and illumination < 87:
                if latest_data.moon_age < HALF_PERIOD:
                    result += '_waxing_gibbous'
                else:
                    result += '_waning_gibbous'
            elif illumination > 87:
                result += '_full'
        return result

#Only one of these per day
class ForecastDay(models.Model):
    """
    Holds the forecast for the next week.
    Basically for a time block of a day
    """
    forecast_date = models.DateField(unique=True)
    location = models.CharField(max_length=50)
    human_location = models.CharField(max_length=50, blank=True, null=True)
    high_temp = models.IntegerField(max_length=4)
    low_temp = models.IntegerField(max_length=4)
    conditions = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    skyicon = models.CharField(max_length=50)
    
    #These will be defined after the above ones.
    sun_rise = models.DateTimeField(null=True, blank=True)
    sun_set = models.DateTimeField(null=True, blank=True)
    moon_illuminated = models.IntegerField(max_length=4, blank=True, null=True)
    moon_age = models.IntegerField(max_length=4, blank=True, null=True)
    
    #This will be fun to hold weather man accountable :)
    #Taken out for now, because it isn't necessary
    #actual_high_temp = models.IntegerField(max_length=4, blank=True, null=True)
    #actual_low_temp = models.IntegerField(max_length=4, blank=True, null=True)
    
    objects = ForecastDayManager()
    
    class Meta:
        ordering = ['-forecast_date']
        get_latest_by = 'forecast_date'
        
    def get_absolute_url(self):
        date = self.forecast_date
        return reverse('forecastday_detail', None, (), {
                'year': date.year,
                'month': date.strftime('%b').lower(),
                'day': date.day,
                'object_id': self.id,
                })
    
    def __unicode__(self):
        return "%s at %s" % (self.location, self.forecast_date)


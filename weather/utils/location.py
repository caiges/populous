from django.conf import settings
import urllib2
import elementtree.ElementTree as ET
from dateutil import parser 
from weather.models import ForecastDay, Forecast
import datetime
import logging
    
def _hour_minute(node):
    return {'hour': int(node.find('hour').text), 'minute': int(node.find('minute').text)}

def get_location():
    return settings.LOCATION

def get_forecast(location_list):
    """
    Gets the upcoming forecast.
    It should be run once a day. It is associated with the ForecastDay model.
    """
    #Might need to munge location to get a query out of it
    location, human_location = location_list
    date = datetime.datetime.today()
    query = location
    url = "http://api.wunderground.com/auto/wui/geo/ForecastXML/index.xml?query=%s" % query
    f = urllib2.urlopen(url)
    xml = f.read()
    root = ET.XML(xml)
    
    forecast = {'location': location, 'human_location': human_location}
    #Find forecast
    simple = root.find('simpleforecast')
    for day in simple.findall('forecastday'):
        forecast['forecast_date'] = parser.parse(day.find('date').find('pretty').text)
        forecast['high_temp'] = day.find('high').find('fahrenheit').text
        forecast['low_temp'] = day.find('low').find('fahrenheit').text
        forecast['conditions'] = day.find('conditions').text
        forecast['icon'] = day.find('icon').text
        forecast['skyicon'] = day.find('skyicon').text
        try:
            f, created = ForecastDay.objects.get_or_create(**forecast)
            if created:
                f.save()
        except:
            logging.info("Long Range Forecast Data missing or already created")
    
        
    #Find Moon
    moon = root.find('moon_phase')
    illuminated = moon.find('percentIlluminated')
    age = moon.find('ageOfMoon')
    sun_rise = datetime.datetime(date.year, date.month, date.day, **_hour_minute(moon.find('sunrise')))
    sun_set = datetime.datetime(date.year, date.month, date.day, **_hour_minute(moon.find('sunset'))) 
    #It doesn't error, so it appears to be doing what it should.
    f = ForecastDay.objects.get(forecast_date=date)
    f.sun_rise = sun_rise
    f.sun_set = sun_set
    f.moon_illuminated = illuminated.text
    f.moon_age = age.text
    try:
        f.save()
    except:
        logging.info("Moon Data missing or no new data available")

    
def get_hourly(location_list):
    """
    Gets a less frequently updated but more informative feed.
    Main difference is that this one grabs the icon for the current weather.
    This should be run once an hour
    """
    location, human_location = location_list
    query = location
    url = "http://api.wunderground.com/auto/wui/geo/WXCurrentObXML/index.xml?query=%s" % query
    f = urllib2.urlopen(url)
    xml = f.read()
    root = ET.XML(xml)
    
    current = {'location': location, 'human_location': human_location}
    current['observation_time'] = parser.parse(root.find('observation_time').text.replace('Last Updated on',''))
    current['temperature'] = root.find('temp_f').text
    current['humidity'] = root.find('relative_humidity').text.strip('%') #Remove %
    current['wind_speed'] = root.find('wind_mph').text
    current['wind_direction'] = root.find('wind_dir').text
    current['icon'] = root.find('icon').text
    current['conditions'] = root.find('weather').text
    try:
        f = Forecast(**current)
        f.save()
    except:
        logging.info("Hourly Forecast Data missing or no new data available")
    
def get_current(location_list):
    """
    Gets your current conditions. It is a bit more flaky because
    it depends on the City and State being correct. However, it will get the
    exactly current up-to-date information.
    """
    import re
    import feedparser
    location, human_location = location_list
    city, state = human_location.split(',')
    url = "http://rss.wunderground.com/auto/rss_full/%s/%s.xml" % (state.strip(), city.strip())
    feed = feedparser.parse(url)
    s = feed.entries[0].summary
    current = {'location': location, 'human_location': human_location}
    
    current['observation_time'] = parser.parse(feed.entries[0].updated)
    temperature = re.compile('Temperature: ([\d\.]+)')
    current['temperature'] = temperature.search(s).group(1)
    humidity = re.compile('Humidity: (\d+)')
    current['humidity'] = humidity.search(s).group(1)
    conditions = re.compile('Conditions: ([\w\s]+)')
    current['conditions'] = conditions.search(s).group(1)
    windspeed = re.compile('Wind Speed: ([\d\.]+)')
    current['wind_speed'] = windspeed.search(s).group(1)
    winddirection = re.compile('Wind Direction: (\w+)')
    current['wind_direction'] = winddirection.search(s).group(1)
    try:
        f = Forecast(**current)
        f.save()
    except:
        logging.info("Current Forecast Data missing or no new data available")
    

    
if __name__ == '__main__':
    get_forecast(get_location())
    get_hourly(get_location())
    get_current(get_location())

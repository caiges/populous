from django.conf.urls.defaults import *
from weather.models import ForecastDay, Forecast
from django.contrib import admin
from django.views.generic.simple import redirect_to
admin.autodiscover()

#Custom views
urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': 'latest/' } ), 
)

#Generic Views
forecastday_dict = {
    'queryset': ForecastDay.objects.all(),
    'date_field': 'forecast_date',
    'allow_future': True,
}

forecast_dict = {
    'queryset': Forecast.objects.all(),
    'date_field': 'observation_time',
}

latest_dict = {
    'queryset': Forecast.objects.all(),
    'object_id': Forecast.objects.latest().id,
    'template_name': 'weather/latest.html'
}

sevenday_dict = {
    'queryset': ForecastDay.objects.get_latest(6),
    'template_name': 'weather/forecast.html',
}

urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^latest/$', 'object_detail', latest_dict, name='latest_weather'),
    url(r'^forecast/$', 'object_list', sevenday_dict, name='latest_forecast'),
    )

#ForecastDay's
urlpatterns += patterns('django.views.generic.date_based',
   url(r'^pastdaily/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<object_id>[-\w]+)/$', 'object_detail', forecastday_dict, 'forecastday_detail'),
   url(r'^pastdaily/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',               'archive_day',   forecastday_dict, 'forecastday_day'),
   url(r'^pastdaily/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                'archive_month', forecastday_dict, 'forecastday_month'),
   url(r'^pastdaily/(?P<year>\d{4})/$',                                                    'archive_year',  forecastday_dict, 'forecastday_year'),
   url(r'^pastdaily/$',                                                                    'archive_index', forecastday_dict, 'forecastday_index'),
)

#Forecasts
urlpatterns += patterns('django.views.generic.date_based',
   (r'^pastcurrent/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<object_id>[-\w]+)/$', 'object_detail', forecast_dict, 'forecast_detail'),
   (r'^pastcurrent/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',               'archive_day',   forecast_dict, 'forecast_day'),
   (r'^pastcurrent/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                'archive_month', forecast_dict, 'forecast_month'),
   (r'^pastcurrent/(?P<year>\d{4})/$',                                                    'archive_year',  forecast_dict, 'forecast_year'),
   (r'^pastcurrent/$',                                                                    'archive_index', forecast_dict, 'forecast_index'),
)

from weather.models import *
from django.contrib import admin

class BaseForecast(admin.ModelAdmin):
    list_filter = ('location',)
    search_fields = ['location', 'human_location']

class ForecastAdmin(BaseForecast):
    date_hierarchy = 'observation_time'
    list_display = ('human_location', 'location', 'observation_time')

class ForecastDayAdmin(BaseForecast):
    date_hierarchy = 'forecast_date'
    list_display = ('human_location', 'location', 'forecast_date')

admin.site.register(Forecast, ForecastAdmin)
admin.site.register(ForecastDay, ForecastDayAdmin)
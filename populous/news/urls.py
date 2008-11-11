from django.conf.urls.defaults import *
from news.models import Story

info_dict = {
    'queryset': Story.objects.approved(),
    'date_field': 'pub_date',
}

urlpatterns = patterns('django.views.generic.date_based',
    url(r'^$',                                                                          'archive_index', info_dict, name="news-archive"),
    url(r'^(?P<year>\d{4})/$',                                                          'archive_year',  info_dict, name="news-archive_year"),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                      'archive_month', info_dict, name="news-archive_month"),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',                     'archive_day',   info_dict, name="news-archive_day"),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',    'object_detail', info_dict, name="news-story_detail"),
)

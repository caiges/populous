from django.conf.urls.defaults import *
from populous.news.models import Story
from populous.news.feeds import CollectionFeed

info_dict = {
    'queryset': Story.objects.approved(),
    'date_field': 'pub_date',
}

feeds = {
    'latest': CollectionFeed,
}

urlpatterns = patterns('',
    #(r'^(?P<url>.*)/feed/$',    'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    #(r'^(?P<url>.*)/$',         'populous.news.views.collection'),
    url(r'^$',                                                                          'django.views.generic.date_based.archive_index', info_dict, name="news-archive"),
    url(r'^(?P<year>\d{4})/$',                                                          'django.views.generic.date_based.archive_year',  info_dict, name="news-archive_year"),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                      'django.views.generic.date_based.archive_month', info_dict, name="news-archive_month"),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',                     'django.views.generic.date_based.archive_day',   info_dict, name="news-archive_day"),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',    'django.views.generic.date_based.object_detail', info_dict, name="news-story_detail"),
)

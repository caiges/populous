from django.conf.urls.defaults import *

urlpatterns = patterns('populous.blogs.views',
    url(r'^collections/(?P<slug>[-\w]+)/$',                                                                 'collection',  name="blogs-collection"),
    url(r'^(?P<blog_slug>[-\w]+)/$',                                                                        'index', name="blogs-entry_index"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/$',                                                        'archive_year',  name="blogs-entry_archive_year"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                    'archive_month', name="blogs-entry_archive_month"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',                   'archive_day',   name="blogs-entry_archive_day"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',  'entry_detail', name="blogs-entry_detail"),
    url(r'^$',                                                                                              'index', name="blogs-index"),
)

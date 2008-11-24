from django.conf.urls.defaults import *

urlpatterns = patterns('populous.blogs.views',
    url(r'^collections/$',                                                                                  'collection_index',   name="blogs-collection_index"),
    url(r'^collections/(?P<slug>[-\w]+)/$',                                                                 'collection_detail',  name="blogs-collection_detail"),
    url(r'^list/$',                                                                                         'blogs_list',         name="blogs-list"),
    url(r'^(?P<blog_slug>[-\w]+)/$',                                                                        'blog_detail',        name="blogs-entry_archive"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/$',                                                        'blog_archive_year',  name="blogs-entry_archive_year"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/$',                                    'blog_archive_month', name="blogs-entry_archive_month"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',                   'blog_archive_day',   name="blogs-entry_archive_day"),
    url(r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',  'blog_entry_detail',  name="blogs-entry_detail"),
    url(r'^$',                                                                                              'blogs_index',        name="blogs-index"),
)


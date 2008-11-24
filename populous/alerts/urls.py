from django.conf.urls.defaults import *

urlpatterns = patterns('populous.alerts.views',
    url(r'^$', 'index', name='alerts-index'),
    url(r'^subscribe/$', 'subscribe', name='alerts-subscribe'),
    url(r'^subscribe/confirm/$', 'confirm', name='alerts-confirm'),
    url(r'^change/(?P<sub_id>\d+)/$', 'change', name='alerts-change'),
    url(r'^remove/(?P<sub_id>\d+)/$', 'remove', name='alerts-remove'),
)
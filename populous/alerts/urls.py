from django.conf.urls.defaults import *

urlpatterns = patterns('populous.alerts',
    (r'^/?$', 'user_alerts'),
    (r'^subscription/(?P<url>[\w-]+)$', 'subscription'),
)
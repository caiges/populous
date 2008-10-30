from django.conf.urls.defaults import *

urlpatterns = patterns('populous.inlines.views.admin',
    url(r'^form/(?P<inline_id>\d+)/$', 'form', name='inlines-admin-form'),
)

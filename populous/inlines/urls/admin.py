from django.conf.urls.defaults import *

urlpatterns = patterns('populous.inlines.views.admin',
    url(r'^render/$', 'render', name='inlines-admin-render'),
    url(r'^(?P<app_label>[-\w]+)/(?P<inline_name>[-\w]+)/form/$', 'form', name='inlines-admin-form'),
)

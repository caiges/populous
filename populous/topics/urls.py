from django.conf.urls.defaults import *
from topics.models import Topic

info_dict = {
    'queryset': Topic.objects.all()
}

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$',                  'object_list', info_dict, name="topics-list"),
    url(r'^(?P<slug>[\w-]+)/$', 'object_detail',  dict(info_dict, slug_field='slug'),  name="topics-detail"),
)
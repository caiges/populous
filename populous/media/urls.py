from django.conf.urls.defaults import *

from populous.media.models import Photo, Video, Gallery, GallerySet

NUM_PER_PAGE = 20

photo_info = {
    'queryset': Photo.on_site.all(),
    'date_field': 'creation_date',
}

video_info = {
    'queryset': Video.on_site.all(),
    'date_field': 'creation_date',
    'paginate_by': NUM_PER_PAGE,
}

urlpatterns = patterns('',
    # Galleries
    url(r'^galleries/$', 'django.views.generic.list_detail.object_list', {'queryset': Gallery.on_site.all()}),
    url(r'^galleries/sets/$', 'django.views.generic.list_detail.object_list', {'queryset': GallerySet.on_site.all()}),
    url(r'^galleries/sets/(?P<slug>[\w-]+)/flash/$', 'populous.media.views.galleries.gallery_set_detail', {'is_flash': True}),
    url(r'^galleries/sets/(?P<slug>[\w-]+)/xml/$', 'populous.media.views.galleries.gallery_set_detail', {'is_xml': True}), 
    url(r'^galleries/sets/(?P<slug>[\w-]+)/$', 'populous.media.views.galleries.gallery_set_detail'), 
    url(r'^galleries/(?P<gallery_slug>[\w-]+)/flash/$', 'populous.media.views.galleries.gallery_detail', {'is_flash': True}),
    url(r'^galleries/(?P<gallery_slug>[\w-]+)/xml/$', 'populous.media.views.galleries.gallery_detail', {'is_xml': True}),
    url(r'^galleries/(?P<gallery_slug>[\w-]+)/$', 'populous.media.views.galleries.gallery_detail'),
    
    # Photos
    url(r'^photos/?$', 'django.views.generic.date_based.archive_index', photo_info),
    url(r'^photos/(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year', photo_info),
    url(r'^photos/(?P<year>\d{4})/(?P<month>\w{3})/$', 'django.views.generic.date_based.archive_month', photo_info),
    url(r'^photos/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$', 'django.views.generic.date_based.archive_day', photo_info),
    url(r'^photos/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<object_id>\d+)/$', 'django.views.generic.date_based.object_detail', photo_info),
    url(r'^photos/latest/$', 'populous.media.views.photos.latest_photos'),
    url(r'^photos/today/$', 'django.views.generic.date_based.archive_today', dict(photo_info, allow_empty=True)),
    url(r'^photos/photographers/(?P<slug>[\w-]+)/$', 'populous.media.views.photos.photographer'),
    
    # Videos
    url(r'^videos/?$', 'django.views.generic.list_detail.object_list', {'queryset': Video.on_site.all(), 'paginate_by': NUM_PER_PAGE}),
    url(r'^videos/xmlhttp/?$', 'populous.media.views.videos.video_list_xmlhttp'),
    url(r'^videos/archives/$', 'django.views.generic.date_based.archive_index', video_info),
    url(r'^videos/archives/(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year', video_info),
    url(r'^videos/archives/(?P<year>\d{4})/(?P<month>\w{3})/$', 'django.views.generic.date_based.archive_month', video_info),
    url(r'^videos/archives/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$', 'django.views.generic.date_based.archive_day', video_info),
    url(r'^videos/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<object_id>[\w-]+)/$', 'django.views.generic.date_based.object_detail', video_info),
    url(r'^videos/(?P<section_url>[\w-]+)/$', 'populous.media.views.videos.video_list_for_category'),
)

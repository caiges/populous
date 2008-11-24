from django.conf import settings
from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib.syndication.views import feed

from populous.news.models import Collection
from populous.news.feeds import CollectionFeed

def collection(request, url):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    
    is_feed = False
    if url.endswith('/feed/'):
        is_feed = True
        url = url[:url.rfind('feed')]

    if not is_feed:
        collection = get_object_or_404(Collection, url=url, sites=Site.objects.get_current())
        t = loader.select_template((
            collection.template_name,
            'news/collections/%s.html' % '_'.join(collection.url.strip('/').split('/')),
            'news/collections/default.html'))
        c = RequestContext(request, {'collection': collection})
        return HttpResponse(t.render(c))
    else:
        return feed(request, url, {'': CollectionFeed})
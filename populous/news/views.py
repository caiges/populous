from django.conf import settings
from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe

from news.models import Collection


def collection(request, url):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    collection = get_object_or_404(Collection, url=url, sites=Site.objects.get_current())
    t = loader.select_template((
        collection.template_name,
        'news/collections/%s.html' % '_'.join(collection.url.strip('/').split('/')),
        'news/collections/default.html'))
    c = RequestContext(request, {'collection': collection})
    return HttpResponse(t.render(c))
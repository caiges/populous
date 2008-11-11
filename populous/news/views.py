from django.conf import settings
from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe

from news.models import Collection

DEFAULT_TEMPLATE = 'news/collection_default.html'

def collection(request, url):
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url
    collection = get_object_or_404(Collection, url=url, sites=Site.objects.get_current())
    if collection.template_name:
        t = loader.select_template((collection.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)
    
    c = RequestContext(request, {
        'collection': collection,
    })
    response = HttpResponse(t.render(c))
    return response
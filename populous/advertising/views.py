from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Template, Context
from django.template.loader import get_template

from populous.advertising.models import ClassifiedCategory

def get_placement_iframe(request):
    """
    Takes a ``Request`` object and returns a rendered placement suitable for inclusion in an iFrame.
    Raises ``Http404`` else.
    """
    if request.GET.get('placement') and request.GET.get('template'):
        vars = request.GET.copy()
        placement = advertising.placements.get_object(pk=vars['placement'])
        template = Template('''
        <html>
            <head>
                <link type="text/css" media="screen" rel="stylesheet" href="http://media.dailybruin.com/dailybruin/css/dailybruin/reset.css" />
                <link type="text/css" media="screen" rel="stylesheet" href="http://media.dailybruin.com/dailybruin/css/dailybruin/ads.css" />
            </head>
            <body>%s</body>
            </html>''' % placement.render(vars['template']))
        return HttpResponse(template.render(None))
    else:
        raise Http404

def add_impression(request):
    if request.GET.get('ad') and request.GET.get('ct') and request.GET.get('pl'):
        vars = request.GET.copy()
        ct = core.contenttypes.get_object(pk=int(vars['ct']))
        ad = ct.get_object_for_this_type(pk=int(vars['ad']))
        placement = advertising.placements.get_object(pk=int(vars['pl']))
        ad.add_clickthrough(placement)
        return HttpResponseRedirect(ad.get_absolute_url())
    else:
        raise Http404

def generic_lookup(request):
    if request.POST.get('content_type_id') and request.POST.get('object_id'):
        vars = request.POST.copy()
        content_type = get_object_or_404(core.contenttypes, pk=vars['content_type_id'])
        object = content_type.get_object_for_this_type(pk=vars['object_id'])
        return HttpResponse(
            "%s" % object.__repr__()[:vars.get('truncate')] or "%s" % object.__repr__()
        )
    else:
        raise Http404

        
def generic_apps_lookup(request):
    content_type_urls = 'APP_URLS = {'
    for ct in core.contenttypes.get_list():
        content_type_urls += "%d: '../../../%s/%s/'," % (ct.id, ct.package_id, ct.python_module_name)
    content_type_urls = '%s};' % content_type_urls[:len(content_type_urls)-1]
    return HttpResponse("%s" % content_type_urls, mimetype="text/plain")

client_html = '''{% for ad in ad_list %}
<li><a href="../../../{{ ad.ad.get_app_name }}/{{ ad.ad.get_module_name }}/{{ ad.ad.id }}/">{{ ad.ad.name }} ({{ ad.type }})</a></li>{% endfor %}
'''
def client_lookup(request):
    if request.POST.get('client_id'):
        vars = request.POST.copy()
        client = get_object_or_404(advertising.clients, pk=vars['client_id'])
        ad_list = []
        for ad in client.get_client_ad_list():
            ad_list.append({
                'ad': ad,
                'type': ad.get_meta_info('verbose_name')
            })
        t = Template(client_html)
        c = Context({
            'ad_list': ad_list,
        })
        return HttpResponse(t.render(c), 'text/html')
    else:
        raise Http404

def classifieds_index(request):
    category_list = ClassifiedCategory.objects.all().order_by('name')
    category_dict = {}
    category_dict['col1'] = category_list[:3]
    category_dict['col2'] = category_list[3:]
    TwoColumnCategories = category_dict
    return render_to_response('advertising/classifieds/index.html', {'TwoColumnCategories': TwoColumnCategories})
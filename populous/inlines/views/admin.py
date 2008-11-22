from django.http import HttpResponse, Http404
from django.db.models import get_model
from populous.inlines.models import RegisteredInline
from populous.inlines.utils import get_inline

import cjson

def form(request, app_label, inline_name):
    try:
        inline = RegisteredInline.objects.get(app_label=app_label, inline_name=inline_name)
    except RegisteredInline.DoesNotExist:
        inline = None
    
    if inline is not None:
        form = inline.inline_class().form
        return HttpResponse(form().render(request))

def render(request):
    inline_id = request.POST['id']
    inline_attrs = cjson.decode(request.POST['attrs'])
    model_app_label = request.POST['model_app_label']
    model_name = request.POST['model_name']
    model_pk = request.POST['model_pk']
    field_name = request.POST['field_name']
    
    app_label, inline_name = inline_attrs.get('type').split('.')
    inline_class = get_inline(app_label, inline_name)
    inline = inline_class(inline_attrs)
    model_class = get_model(model_app_label, model_name)
    model = model_class._default_manager.get(pk=model_pk)
    field = model._meta.get_field(field_name)
    
    rendered_inline = inline.render(request, model, field)
    return HttpResponse(rendered_inline)
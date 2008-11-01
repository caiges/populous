from django.http import HttpResponse, Http404
from populous.inlines.models import RegisteredInline

def form(request, app_label, inline_name):
    #try:
    inline = RegisteredInline.objects.get(app_label=app_label, inline_name=inline_name)
    #except:
    #    inline = None
    
    if inline is not None:
        form = inline.inline_class().get_form(request, None, None)
        return HttpResponse(form().render(request))
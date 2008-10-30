from django.http import HttpResponse, Http404
from populous.inlines.models import RegisteredInline

def form(request, inline_id):
    try:
        inline = RegisteredInline.objects.get_inline()
    except:
        inline = None
    
    if inline is not None:
        form = inline.get_form(request)
    
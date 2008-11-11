from django.conf import settings
from django.contrib.sites.models import Site

def extra(request):
    try:
        google_analytics = settings.GOOGLE_ANALYTICS
    except:
        google_analytics = ''
    
    site = Site.objects.get_current()
    
    return {
        'SITE': site,
        'GOOGLE_ANALYTICS': google_analytics,
    }
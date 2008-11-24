from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from populous.alerts.models import Subscription
from populous.alerts.forms import SubscribeFromFeedForm, SubscribeForm

def index(request):
    t = loader.get_template('alerts/index.html')
    c = RequestContext(request, {
        'subscriptions': Subscription.objects.filter(user=request.user)
    })
    return HttpResponse(t.render(c))

def subscribe(request):
    if not request.method == "POST":
        return HttpResponseRedirect(reverse(index))

    data = request.POST.copy()
    
    if request.META.get('HTTP_REFERER').endswith(reverse(subscribe)):
        # We have been POSTed to from ourself
        form = SubscribeForm(data)
        if form.is_valid():
            pass
    else:
        # Check to see if we've been posted to with a proper    
        feed_url = data.get('feed_url')
        form = SubscribeFromFeedForm(feed_url, data)
        if form.is_valid():
            # Do something fun now...
            pass
        
    t = loader.get_template('alerts/subscribe.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def change(request, sub_id):
    pass

def remove(request, sub_id):
    pass

def confirm(request):
    pass
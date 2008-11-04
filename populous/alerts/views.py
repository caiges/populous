from datetime import datetime
from django import newforms as forms
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.localflavor.us.forms import USPhoneNumberField as PhoneNumberField
from django.contrib.sites.models import Site
from django.contrib.syndication.views import feed
from django.template import loader
from django.template.context import RequestContext, Context
from django.utils.translation import ugettext
from django.utils.translation import ugettext as _

from populous.alerts.models import Alert, Subscription, FREQUENCY_CHOICES
from populous.alerts.registered import ALERT_DICT
from populous.sms.models import Provider

# Templates
INDEX_TEMPLATE = 'alerts/index.html'
SUBSCRIBE_TEMPLATE = 'alerts/subscribe.html'
CONFIRM_SUBSCRIPTION_TEMPLATE = 'alerts/confirm.html'
MODIFY_TEMPLATE = 'alerts/modify.html'

def _make_bool(val):
    if val == 'on':
        return True
    if val == 'off':
        return False
    return val

@login_required
def user_alerts(request, slug):
    t = loader.get_template(INDEX_TEMPLATE)
    c = RequestContext(request, {
        'alerts': Alert.objects.filter(user=request.user),
        'subscriptions': Subscription.objects.filter(user=request.user),
    })
    return HttpResponse(t.render(c))

class Subscribe(forms.Form):
    frequency = forms.ChoiceField(label=_('Frequency'), choices=FREQUENCY_CHOICES, initial=1)
    via_email = forms.BooleanField(label=_('via e-Mail'), required=False)
    allow_html = forms.BooleanField(label=_('Accept HTML formatted e-Mails'), required=False)
    email_address = forms.EmailField(label=_('e-Mail address'), required=False)
    via_sms = forms.BooleanField(label=_('via SMS'), required=False)
    sms_number = PhoneNumberField(label=_('Phone number for SMS messages'), required=False)
    sms_provider = forms.ModelChoiceField(queryset=Provider.objects.all(), label=_('Mobile provider for SMS messages'), required=False)
    #via_im = forms.BooleanField(label=_('via Instant Messenger'), required=False)
    
    def clean(self):
        if not self.data.get('via_email', False) and not self.data.get('via_sms', None):
            raise forms.ValidationError(ugettext('You must select at least one form of alert to recieve.'))
        if self.data.get('via_email', False) and not self.data.get('email_address', None):
            raise forms.ValidationError(ugettext('To recieve e-mail alerts, you must enter an e-mail address.'))
        if self.data.get('via_sms', False) and (not self.data.get('sms_number', None) or not self.data.get('sms_provider', None)):
            raise forms.ValidationError(ugettext('To recieve SMS alerts, you must enter a phone number and select a mobile provider.'))
        return self.cleaned_data
    
    def save(self, request):
        try:
            sms_provider = Provider.objects.get(pk=int(self.data.get('sms_provider')))
        except:
            sms_provider = None
        Subscription.objects.create(
            user = request.user,
            url = request.path,
            last_sent_time = datetime.now(),
            frequency = self.data.get('frequency'),
            via_email = _make_bool(self.data.get('via_email', False)),
            allow_html = _make_bool(self.data.get('allow_html', False)),
            email_address = self.data.get('email_address', None),
            via_sms = _make_bool(self.data.get('via_sms', False)),
            sms_number = self.data.get('sms_number', None),
            sms_provider = sms_provider,
            #via_im = self.data.get('via_im', False),
            site = Site.objects.get_current()
        ).execute(request)
        if _make_bool(self.data.get('via_email', False)):
            s=Subscription.objects.get(user=request.user, url=request.path)
            s.send_confirmation_code('email')
        if _make_bool(self.data.get('via_sms', False)):
            s=Subscription.objects.get(user=request.user, url=request.path)
            s.send_confirmation_code('sms')
    
    def modify(self, request, sub):
        sms_provider = None
        if self.data.get('sms_provider', False):
            try:
                sms_provider = Provider.objects.get(pk=self.data.get('sms_provider'))
            except:
                pass
        prev_via_email = sub.via_email
        prev_email_address = sub.email_address
        prev_via_sms = sub.via_sms
        prev_sms_number = sub.sms_number
        sub.frequency = self.data.get('frequency', 1)
        sub.via_email = _make_bool(self.data.get('via_email', False))
        sub.allow_html = _make_bool(self.data.get('allow_html', False))
        sub.email_address = self.data.get('email_address', None)
        sub.via_sms = _make_bool(self.data.get('via_sms', False))
        sub.sms_number = self.data.get('sms_number', None)
        sub.sms_provider = sms_provider
        #sub.via_im = self.data.get('via_im', False)
        
        # If the e-mail address changes, set email_confirmed to False
        if sub.email_address != prev_email_address:
            prev_via_email = False
            sub.email_confirmed = False
            sub.confirmation_code_email = ''
        # If the sms number changes, set sms_confirmed to False
        if sub.sms_number != prev_sms_number:
            prev_via_sms = False
            sub.sms_confirmed = False
            sub.confirmation_code_sms = ''
        sub.save()
        # If the alerts uses e-mail and is not confirmed, send a confirmation code
        if sub.via_email and not sub.email_confirmed and not prev_via_email:
            sub.send_confirmation_code('email')
        # If the alerts uses sms and is not confirmed, send a confirmation code
        if sub.via_sms and not sub.sms_confirmed and not prev_via_sms:
            sub.send_confirmation_code('sms')

@login_required
def subscription(request, url):
    # Start with error checking
    if Subscription.objects.filter(user=request.user, url=request.path, site=Site.objects.get_current()):
        return HttpResponseRedirect('/accounts/%s/alerts/' % request.user.username)
    
    # TODO: Verify alert feed's existanace
    
    if request.method == 'POST':
        form = Subscribe(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect('/accounts/%s/alerts/' % request.user.username)
    else:
        form = Subscribe()
    t = loader.get_template(SUBSCRIBE_TEMPLATE)
    c = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(t.render(c))

class Confirm(forms.Form):
    email_code = forms.CharField(label=_('e-Mail Confirmation Code'), required=False)
    sms_code = forms.CharField(label=_('SMS Confirmation Code'), required=False)
    
    def save(self, request, sub):
        if self.data.get('email_code', False) and self.data.get('email_code', False) == str(sub.confirmation_code_email):
            sub.email_confirmed = True
        if self.data.get('sms_code', False) and self.data.get('sms_code', False) == str(sub.confirmation_code_sms):
            sub.sms_confirmed = True
        sub.save()

@login_required
def confirm_subscription(request, id, slug):
    try:
        s = Subscription.objects.get(pk=id, user=request.user)
    except Subscription.DoesNotExist:
        raise Http404, "No subscription with the id %s for the user %s exists." % (id, request.user)
    
    if request.method == 'POST':
        form = Confirm(request.POST)
        if form.is_valid():
            form.save(request, s)
            return HttpResponseRedirect('/accounts/%s/alerts/' % request.user.username)
    else:
        form = Confirm()
    
    t = loader.get_template(CONFIRM_SUBSCRIPTION_TEMPLATE)
    c = RequestContext(request, {
        'form': form,
        'sub': s,
    })
    return HttpResponse(t.render(c))

@login_required
def resend_confirmation_codes(request, id, slug):
    try:
        s = Subscription.objects.get(pk=id, user=request.user)
    except Subscription.DoesNotExist:
        raise Http404, "No subscription with the id %s for the user %s exists." % (id, request.user)
    
    if s.via_email and not s.email_confirmed:
        s.send_confirmation_code('email')
    # If the alerts uses sms and is not confirmed, send a confirmation code
    if s.via_sms and not s.sms_confirmed:
        s.send_confirmation_code('sms')
    
    return HttpResponseRedirect('/accounts/%s/alerts/' % request.user.username)

@login_required
def change_subscription(request, id, slug):
    try:
        s = Subscription.objects.get(pk=id, user=request.user)
    except Subscription.DoesNotExist:
        raise Http404, "No subscription with the id %s for the user %s exists." % (id, request.user)
    
    if request.method == 'POST':
        form = Subscribe(request.POST)
        if form.is_valid():
            form.modify(request, s)
            return HttpResponseRedirect('/accounts/%s/alerts/' % request.user.username)
    else:
        try:
            sms = s.sms_provider.id
        except:
            sms = None
        form = Subscribe({
            'frequency': int(s.frequency),
            'via_email': s.via_email,
            'allow_html': s.allow_html,
            'email_address': s.email_address,
            'via_sms': s.via_sms,
            'sms_number': s.sms_number,
            'sms_provider': sms,
            #'via_im': s.via_im,
        })
    
    t = loader.get_template(MODIFY_TEMPLATE)
    c = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(t.render(c))

@login_required
def remove_subscription(request, id, slug):
    try:
        s = Subscription.objects.get(pk=id, user=request.user)
    except:
        raise Http404, "No subscription with the id %s for the user %s exists." % (id, request.user)
    s.delete()
    return HttpResponseRedirect('/accounts/%s/alerts/' % request.user.username)
from django import forms
from django.conf import settings
from django.utils.hashcompat import sha_constructor

from populous.alerts.models import Subscription

class SubscribeFromFeedForm(forms.Form):
    feed_ur = forms.URLField(widget=forms.HiddenInput)
    security_hash = forms.CharField(min_length=40, max_length=40, widget=forms.HiddenInput)
    
    def __init__(self, feed_url, data=None, initial=None):
        self.feed_url = feed_url
        if initial is None:
            initial = {}
        initial.update(self.generate_security_data())
        super(SubscribeFromFeedForm, self).__init__(data=data, initial=initial)
    
    def clean_security_hash(self):
        security_hash_dict = {
            'feed_url': self.data.get("feed_url", "")
        }
        expected_hash = self.generate_security_hash(**security_hash_dict)
        actual_hash = self.cleaned_data["security_hash"]
        if expected_hash != actual_hash:
            raise forms.ValidationError("Security hash check failed.")
        return actual_hash
    
    def generate_security_data(self):
        """Generate a dict of security data for "initial" data."""
        security_dict = {
            'feed_url': str(self.feed_url),
            'security_hash': self.initial_security_hash(),
        }
        return security_dict
    
    def initial_security_hash(self):
        initial_security_dict = {
            'feed_url': str(self.feed_url)
        }
        return self.generate_security_hash(**initial_security_dict)
    
    def generate_security_hash(self, feed_url):
        info = (feed_url, settings.SECRET_KEY)
        return sha_constructor("".join(info)).hexdigest()

class SubscribeForm(forms.ModelForm):
    feed_url = forms.URLField(widget=forms.HiddenInput)
    
    class Meta:
        model = Subscription
        fields = ('title', 'frequency', 'via_email', 'email_address',
            'allow_html', 'via_sms', 'sms_number', 'sms_provider')
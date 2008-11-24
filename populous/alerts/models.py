from datetime import datetime, timedelta
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.localflavor.us.models import PhoneNumberField

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from populous.messaging.models import SMSProvider

from populous.alerts.utils import parse_feed


FREQUENCY_CHOICES = (
    (60*60,         'Hourly'),
    (60*60*12,      'Twice Daily'),
    (60*60*24,      'Daily'),
    (60*60*24*7,    'Weekly'),
)

class SubscriptionManager(models.Manager):
    def due(self):
        """
        Returns a queryset of all ``Subcription`` objects that are due
        to be sent.
        """
        import operator
        lookups = []
        for frequency, name in FREQUENCY_CHOICES:
            time = datetime.now() - timedelta(seconds=frequency)
            lookups.append(models.Q(frequency=frequency, last_sent_time__lte=time))
        return self.filter(reduce(operator.or_, lookups))
    
    def send_due(self, fail_silently=True):
        """
        Sends an alerts to each user who has a due ``Subscription`` if there are new items
        for their subscription.
        
        *NOTE*: This can potentially take awhile to complete because it will potentially
        create quite a few remote connections.  This should probably be run by cron once
        or twice an hour.
        """
        feed_cache = {}
        for subscription in self.due():
            feed_url = subscription.feed_url
            if not feed_cache.has_key(feed_url):
                # Check the feed
                feed_cache[feed_url] = parse_feed(feed_url, fail_silently)
            subscription.send_alert(feed_cache.get(feed_url))
                
                

class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    title = models.CharField(_('title'), max_length=500)
    feed_url = models.CharField(_('feed URL'), max_length=200, help_text=_('This should be a valid feed url.'))
    frequency = models.FloatField(_('maximum frequency'), choices=FREQUENCY_CHOICES, default=60*60*24)
    site = models.ForeignKey(Site, blank=True)
    last_sent_time = models.DateTimeField(_('last sent time'), auto_now_add=True)
    last_item_date = models.DateTimeField(_('most recent item'), auto_now_add=True)
    
    # E-mail
    via_email = models.BooleanField(_('Send via e-mail'), blank=True, null=True, default=False)
    email_address = models.EmailField(_('E-mail address'), blank=True)
    allow_html = models.BooleanField(_('Recieve HTML e-mail'), blank=True, null=True, default=True)
    email_confirmed = models.BooleanField(_('E-mail address has been confirmed'), blank=True, null=True, default=False)
    confirmation_code_email = models.CharField(_('confirmation code (e-mail)'), max_length=32, blank=True)
    
    # SMS
    via_sms = models.BooleanField(_('Send via SMS'), blank=True, null=True, default=False)
    sms_number = PhoneNumberField(_('Phone number for SMS messages'), blank=True)
    sms_provider = models.ForeignKey(SMSProvider, blank=True, null=True, verbose_name=_('SMS Provider'))
    sms_confirmed = models.BooleanField(_('Mobile number has been confirmed'), blank=True, null=True, default=False)
    confirmation_code_sms = models.CharField(_('confirmation code (SMS)'), max_length=6, blank=True)
    
    objects = SubscriptionManager()
    
    def __unicode__(self):
        return self.title
    
    def needs_confirmation(self):
        needs_confirmation = 0
        if self.via_email and self.confirmation_code_email and not self.email_confirmed:
            needs_confirmation += 1
        if self.via_sms and self.confirmation_code_sms and not self.sms_confirmed:
            needs_confirmation += 1
        return needs_confirmation
    
    def send_alert(self, items):
        """
        Send an alert if there are any items in ``items`` that have a newer
        ``pub_date`` than the most recently recorded ``last_item_date``.
        """
        from populous.messaging import EmailMessage
        for item in items:
            if item.get('pub_date') > self.last_item_date:
                if self.via_email and self.email_confirmed:
                    email = EmailMessage(subject=self.title, body='There was a new item posted to %s' % self.title,
                        from_email='HappyAlertBot@demo.populousproject.com', to=[self.email_address])
                    email.send(fail_silently=False)
                
                # TODO: Other messaging schemes
                return
    
    def send_confirmation_code(self, msg_type):
        from django.core.mail import EmailMessage
        if msg_type == 'email':
            SUBJECT = 'Your e-mail alert confirmation code for %s' % self.site.name
            if not self.confirmation_code_email:
                self.confirmation_code_email = self.get_random_confirmation_code_email()
                self.save()
            if self.allow_html:
                c = Context({
                    'code': self.confirmation_code_email,
                    'site': self.site
                })
                t = loader.get_template('alerts/confirmation_email.html')
                email_response = HttpResponse(t.render(c))
            else:
                email_response = '''Your e-mail alert confirmation code is:\n\n\t\t%s''' % (self.confirmation_code_email)
            return EmailMessage(to=[self.email_address], subject=SUBJECT, body=email_response).send()
        if msg_type == 'sms':
            SUBJECT = '''SMS alert confirmation code'''
            if not self.confirmation_code_sms:
                self.confirmation_code_sms = self._get_random_confirmation_code_sms()
                self.save()
            sms_response = '''SMS alert confirmation code for %s is: "%s"''' % (self.site.name, self.confirmation_code_sms)
            return EmailMessage(to=[self.sms_provider.get_email_address(self.sms_number)], subject=SUBJECT, body=sms_response).send()
    
    @classmethod
    def get_random_confirmation_code_email(cls):
        "Generates and returns a random 32-character string that's not in use."
        import md5, random
        while 1:
            code = md5.new(str(random.random())).hexdigest()
            try:
                cls.objects.get(confirmation_code_email=code)
            except cls.DoesNotExist:
                break
        return code

    @classmethod
    def get_random_confirmation_code_sms(cls):
        "Generates and returns a random 6-character string that's not in use."
        import md5, random
        while 1:
            code = md5.new(str(random.random())).hexdigest()[0:6]
            try:
                cls.objects.get(confirmation_code_sms=code)
            except cls.DoesNotExist:
                break
        return code
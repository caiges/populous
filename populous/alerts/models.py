from django.db import models
from django.http import HttpResponse
from django.template import Context, loader
from django.utils.translation import ugettext as _
from django.contrib.localflavor.us.models import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from populous.sms.models import Provider

FREQUENCY_CHOICES = (
    (0, 'Hourly'),
    (0.5, 'Twice Daily'),
    (1, 'Daily'),
    (7, 'Weekly'),
)

class SubscriptionManager(models.Manager):
    def execute_due(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
        SELECT a.*
        FROM alerts_subscription AS a, alerts_subscription AS b
        WHERE
            a.id = b.id
            AND
            (
                extract( days from age( now(), a.last_sent_time ) ) +
                extract( hours from age( now(), a.last_sent_time ) ) / 24
            )
            >= b.frequency
            AND 
            (
                ( a.via_sms = True AND a.sms_confirmed = True )
                OR
                ( a.via_email = True AND a.email_confirmed = True )
            )
        """)
        result_list = []
        for row in cursor.fetchall():
            p = Subscription.objects.get(id=row[0], user=User.objects.get(pk=row[1]), url=row[2])
            result_list.append(p)
        for result in result_list:
            print result
            result.execute()

class Alert(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'))
    url = models.CharField(_('Alert URL'), max_length=200)
    send_time = models.DateTimeField(_('Send time'))
    site = models.ForeignKey(Site, blank=True, verbose_name=_('Site'))
    
    # E-mail
    via_email = models.BooleanField(_('Send via e-mail'), blank=True, null=True, default=False)
    email_address = models.EmailField(_('E-mail address'), blank=True)
    allow_html = models.BooleanField(_('Recieve HTML e-mail'), blank=True, null=True, default=True)
    
    # SMS
    via_sms = models.BooleanField(_('Send via SMS'), blank=True, null=True, default=False)
    mobile_number = PhoneNumberField(_('Phone number for SMS messages'), blank=True)
    provider = models.ForeignKey(Provider, blank=True, null=True, verbose_name=_('SMS Provider'))
    
    # Instant Messanger
    # TODO: Impliment This
    #via_im = models.BooleanField(_('Send via IM'), blank=True, null=True, default=False)
    #screen_name = models.CharField(blank=True)
    #messanger_service = models.CharField(choices=IM_PROVIDERS, blank=True)
    
    def __unicode__(self):
        return u'An Alert'
    
    def execute(self):
        pass

class Subscription(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    url = models.CharField(_('alert URL'), max_length=200)
    slug = models.CharField(max_length=100)
    param = models.CharField(max_length=200)
    frequency = models.FloatField(_('maximum frequency'), choices=FREQUENCY_CHOICES, default=1)
    site = models.ForeignKey(Site, blank=True)
    last_sent_time = models.DateTimeField(_('last sent time'), auto_now=True)
    last_sent_content = models.ForeignKey(ContentType, blank=True, null=True, verbose_name=_('last sent content type'))
    last_sent_obj_id = models.PositiveIntegerField(_('last sent object ID'), blank=True, null=True)
    
    # E-mail
    via_email = models.BooleanField(_('Send via e-mail'), blank=True, null=True, default=False)
    email_address = models.EmailField(_('E-mail address'), blank=True)
    allow_html = models.BooleanField(_('Recieve HTML e-mail'), blank=True, null=True, default=True)
    email_confirmed= models.BooleanField(_('E-mail address has been confirmed'), blank=True, null=True, default=False)
    confirmation_code_email = models.CharField(_('confirmation code (e-mail)'), max_length=32, blank=True)
    
    # SMS
    via_sms = models.BooleanField(_('Send via SMS'), blank=True, null=True, default=False)
    sms_number = PhoneNumberField(_('Phone number for SMS messages'), blank=True)
    sms_provider = models.ForeignKey(Provider, blank=True, null=True, verbose_name=_('SMS Provider'))
    sms_confirmed = models.BooleanField(_('Mobile number has been confirmed'), blank=True, null=True, default=False)
    confirmation_code_sms = models.CharField(_('confirmation code (SMS)'), max_length=6, blank=True)
    
    # Instant Messenger
    #via_im = models.BooleanField(_('send via IM'), blank=True, null=True, default=False)
    
    # Managers
    objects = SubscriptionManager()
    
    def __unicode__(self):
        return u"%s - %s" % (self.slug, self.param)
    
    def save(self):
        alert_url = self.url.split('/', 2)[2]
        try:
            self.slug, self.param = alert_url.split('/', 1)
        except ValueError:
            self.slug, self.param = alert_url, ''
        super(Subscription, self).save()
    
    def execute(self, request=None):
        if request == None:
            from django.http import HttpRequest
            request = HttpRequest
            request.path = self.url
        
        from populous.alerts.registered import ALERT_DICT
        # Determine the alert class
        alert = ALERT_DICT[self.slug](self.slug, self.param, request)
        
        # Send the alert
        send_time, last_sent_obj_id = alert.send(self)
        
        print "%s %s" % (send_time, last_sent_obj_id)
        if send_time and last_sent_obj_id:
            self.last_sent_time = send_time
            self.last_sent_obj_id = last_sent_obj_id
            self.save()
    
    def needs_confirmation(self):
        needs_confirmation = 0
        if self.via_email and self.confirmation_code_email and not self.email_confirmed:
            needs_confirmation += 1
        if self.via_sms and self.confirmation_code_sms and not self.sms_confirmed:
            needs_confirmation += 1
        return needs_confirmation
    
    def send_confirmation_code(self, type):
        CONFIRMATION_EMAIL_TEMPLATE = 'alerts/confirmation_email.html'
        from django.core.mail import EmailMessage
        if type == 'email':
            SUBJECT = '''Your e-mail alert confirmation code for %s''' % self.site.name
            if not self.confirmation_code_email:
                self.confirmation_code_email = self._get_random_confirmation_code_email()
                self.save()
            if self.allow_html:
                c = Context({
                    'code': self.confirmation_code_email,
                    'site': self.site
                })
                t = loader.get_template(CONFIRMATION_EMAIL_TEMPLATE)
                email_response = HttpResponse(t.render(c))
            else:
                email_response = '''Your e-mail alert confirmation code is:\n\n\t\t%s''' % (self.confirmation_code_email)
            return EmailMessage(to=[self.email_address], subject=SUBJECT, body=email_response).send()
        if type == 'sms':
            SUBJECT = '''SMS alert confirmation code'''
            if not self.confirmation_code_sms:
                self.confirmation_code_sms = self._get_random_confirmation_code_sms()
                self.save()
            sms_response = '''SMS alert confirmation code for %s is: "%s"''' % (self.site.name, self.confirmation_code_sms)
            return EmailMessage(to=[self.sms_provider.get_email_address(self.sms_number)], subject=SUBJECT, body=sms_response).send()
    
    def _get_random_confirmation_code_email(cls):
        "Generates and returns a random 32-character string that's not in use."
        import md5, random
        while 1:
            code = md5.new(str(random.random())).hexdigest()
            try:
                cls.objects.get(confirmation_code_email=code)
            except cls.DoesNotExist:
                break
        return code
    _get_random_confirmation_code_email = classmethod(_get_random_confirmation_code_email)

    
    def _get_random_confirmation_code_sms(cls):
        "Generates and returns a random 6-character string that's not in use."
        import md5, random
        while 1:
            code = md5.new(str(random.random())).hexdigest()[0:6]
            try:
                cls.objects.get(confirmation_code_sms=code)
            except cls.DoesNotExist:
                break
        return code
    _get_random_confirmation_code_sms = classmethod(_get_random_confirmation_code_sms)
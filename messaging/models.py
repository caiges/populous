from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class QueuedMessage(models.Model):
    protocol_id = models.CharField(max_length=100)
    protocol = models.CharField(max_length=200)
    sender = models.CharField(max_length=800)
    recipient = models.CharField(max_length=800)
    message = models.TextField()
    subject = models.CharField(max_length=400, blank=True)
    date_queued = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s: %s to %s" % (self.protocol, self.sender, self.recipient)

class SMSProvider(models.Model):
    """
    A provider is the name and e-mail domain of a cellular provider.  This information is used to 'text' phones SMS alerts (via e-mail).
    
    # Create some providers
    >>> teleflip = SMSProvider.objects.create(name="Teleflip", domain="teleflip.com")
    >>> virgin_mobile = SMSProvider.objects.create(name="Virgin Mobile", domain="vmobl.com")
    
    # Form e-mails from phone numbers
    >>> teleflip.get_email_address('123-456-7890')
    '1234567890@teleflip.com'
    >>> virgin_mobile.get_email_address('1234567890')
    '1234567890@vmobl.com'
    
    """

    name = models.CharField(_('provider name'), max_length=100)
    domain = models.CharField(_('e-mail domain'), max_length=200)
    
    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_email_address(self, phone_number):
        """
        Given a phone number, returns the e-mail address to contact that person
        via SMS on this Provider.
        """
        import re
        return '%s@%s' % (re.sub(r'[^\d]', '', phone_number), self.domain)

class IMProtocol(models.Model):
    protocol_id = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name

class SMSProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')
    search_fields = ('name', 'domain')

admin.site.register(SMSProvider, SMSProviderAdmin)
admin.site.register(IMProtocol)

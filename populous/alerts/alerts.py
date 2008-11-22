from datetime import datetime, timedelta
from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.http import HttpResponse
from django.template import Context, loader

class Alert(object):
    """
    The base ``Alert`` class which can be used for building a custom ``Alert`` from
    scratch.  *NOTE*: If you choose to build an ``Alert`` from scratch, rather than
    using the ``AlertForFeed`` class, you must make sure to define the following
    methods:
    
        * TODO: figure out which method/attributes we want to use, both custom ones
            as well as ones which can be overwritten by a ``Feed`` class.
    """
    description_template = "alerts/description.html"
    
    from django.conf import settings
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = "A new alert from %s" % Site.objects.get_current().name
    
    def __init__(self, slug, param, request):
        self.slug = slug
        self.bits = param.rstrip('/').split('/')
        self.request = request
        self.obj = self.get_object()
        
        self.alert_email_template = "alerts/%s_email_alert.html" % slug
        self.alert_sms_template = "alerts/%s_sms_alert.html" % slug
    
    def get_object(self):
        return "An object"
    
    def title(self):
        return "Title"
    
    def link(self):
        return "Link"
    
    def description(self):
        return "This is a description of an alert."
    
    def items(self):
        return "Items"
    
    def render(self, subscription, new_items):
        c = Context({
            'items': new_items,
            'user': subscription.user,
            'site': subscription.site
        })
        
        email_response = None
        sms_response = None
        im_response = None
        
        if subscription.via_email:
            t = loader.get_template(self.alert_email_template)
            email_response = HttpResponse(t.render(c))
        if subscription.via_sms:
            t = loader.get_template(self.alert_sms_template)
            sms_response = HttpResponse(t.render(c))
        #if subscription.via_im:
        #    # TODO: Impliment this
        return email_response, sms_response, im_response
    
    def send(self, subscription):
        """
        Requires ``subscription`` which should be an ``alert.Subscription`` model.
        Calculates which objects are new for this ``subscription`` and sends an alert
        to the user of the proper type (email and/or sms).
        
        Returns a tuple in the format:
            ``(object_id, time_sent)``
        where ``object_id`` is the id of the most recent object and ``time_sent`` is a
        ``datetime`` object of when this alert was sent.
        """
        
        send_time = datetime.now() # Set now so processing time does not affect possible new entries
        
        # Retrive items from feed
        items = list(self.items())
        print items
        if not items:
            print "No items to send"
            return None, None
        
        # Initialize last_sent_content and last_sent_obj_id if they don't exist
        if not subscription.last_sent_content or not subscription.last_sent_obj_id:
            from django.contrib.contenttypes.models import ContentType
            subscription.last_sent_content = ContentType.objects.get_for_model(items[0])
            subscription.last_sent_obj_id = items[0]._meta.pk.value_from_object(items[0])
            subscription.save()
            print "No content Initialized"
            return None, None
        
        # Check to see if enough time has passed to send another alert
        if subscription.last_sent_time + timedelta(days=subscription.frequency) > send_time:
            print "It's too soon still"
            return None, None
        
        # Determine new items
        last_item = subscription.last_sent_content.get_object_for_this_type(id=subscription.last_sent_obj_id)
        print last_item
        last_item_index = items.index(last_item)
        print last_item_index
        new_items = items[:last_item_index]
        print new_items
        
        # Render messages to send
        #   Messages is a tupple with three items: (e_mail response, sms response, IM response)
        if new_items:
            messages = self.render(subscription, new_items)
            print messages[0]
            print messages[1]
            print messages[2]
        else:
            print "No new items"
            return None, None
        
        # If there are messages to send, send them
        from django.core.mail import send_mail
        messages_sent = 0
        if messages[0] and subscription.email_confirmed:
            messages_sent += send_mail(self.subject, messages[0], self.from_email, [str(subscription.user.email)])
        if messages[1] and subscription.sms_confirmed:
            to_email = subscription.sms_provider.get_email_address(subscription.sms_number)
            messages_sent += send_mail(self.subject, messages[1], self.from_email, [to_email])
        if messages[2]:
            # TODO: Impliment this sending an IM
            pass
        
        # If no messages could be sent, return (None, None)
        if messages_sent == 0:
            print "No messages sent"
            return None, None
        
        return send_time, new_items[0].id

class AlertForFeed(Alert):
    """
    This class can be used to create an ``Alert`` from a pre-existing ``Feed`` class.
    In order to do so, you must define ``feed_class`` which should be a valid
    ``django.contrib.syndication.feeds.Feed`` class.
    """
    feed_class = None
    
    def __init__(self, slug, param, request):
        super(AlertForFeed, self).__init__(slug, param, request)
        self.feed = self.__get_feed()
        self.obj = self.__get_obj()
    
    def __get_feed(self):
        if self.feed_class is None:
            raise ImproperlyConfigured, "You must define a feed_class."
        return self.feed_class(self.slug, self.request)
    
    def __get_obj(self):
        if self.bits:
            try:
                return self.feed.get_object(self.bits)
            except TypeError:
                # get_object doesn't accept bits
                print "Uh-oh, get_object doesn't accept bits"
                return None
        else:
            return None
    
    def items(self):
        return self.feed.items(self.obj)
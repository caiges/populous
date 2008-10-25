import dbus
from populous.messaging.protocols.base import BaseMessage
from populous.messaging.concierge.exceptions import ConciergeError
from populous.messaging.concierge.connection import setup_dbus    

class IMConnection(object):   
    def __init__(self, fail_silently=False):
        self.fail_silently = fail_silently
        self.accounts = []
        self.connection = None
    
    def open(self):
        if self.connection:
            return False
        try:
            # Try to connect to the concierge daemon via dbus
            setup_dbus() # This properly sets the `DBUS_SESSION_BUS_ADDRESS` environ variable so that dbus will work
            self.bus = dbus.SessionBus()
            self.obj = self.bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
            self.connection = dbus.Interface(self.obj, "im.pidgin.purple.PurpleInterface")
            return True
        except:
            if not self.fail_silently:
                raise ConciergeError('Could not connect to concierge daemon.  Is it running?')
    
    def send_messages(self, messages):
        if not messages:
            return
        new_conn_created = self.open()
        if not self.connection:
            # We failed silently on open(). Trying to send would be pointless.
            return
        num_sent = 0
        for message in messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        if new_conn_created:
            #self.close()
            pass
        return num_sent
    
    def _get_account_by_protocol(self, protocol):
        """
        Lookup the available protocols and cache them.
        
        Returns the account matching the passed ``protocol``.  Note that what is returned
        is a `dbus` value representing the approriate account.  Returns `None` if ``protocol``
        isn't available.
        """
        if not hasattr(self, '__protocol_dict'):
            protocol_dict = {}
            for account in self.connection.PurpleAccountsGetAll():
                proto = unicode(self.connection.PurpleAccountGetProtocolName(account))
                protocol_dict[proto] = account
            setattr(self, '__protocol_dict', protocol_dict)
        try:
            return getattr(self, '__protocol_dict')[protocol]
        except KeyError:
            return None
    
    def _send(self, message):
        """A helper method that does the actual sending."""
        if not message.to:
            return False
        try:
            for protocol, username in message.to:
                account = self._get_account_by_protocol(protocol)
                conv = self.connection.PurpleFindConversationWithAccount(1, username, account)
                if not conv:
                    # No conversation exists, so start a new one
                    conv = self.connection.PurpleConversationNew(1, account, username)
                self.connection.PurpleConversationPresent(conv)
                im = self.connection.PurpleConvIm(conv)
                self.connection.PurpleConvImSend(im, message.body)
        except:
            if not self.fail_silently:
                raise
            return False
        return True

class IMMessage(BaseMessage):
    def __init__(self, subject='', body='', to=None, connection=None, attachments=None):
        from populous.messaging import im_connection
        if to:
            assert not isinstance(to, basestring), '"to" argument must be a list or tuple'
            self.to = to
        else:
            self.to = []
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.connection = connection or im_connection
    
    def get_connection(self, fail_silently=False):
        if not self.connection:
            self.connection = IMConnection(fail_silently=fail_silently)
        return self.connection
    
    def send(self, fail_silently=False):
        return self.get_connection(fail_silently).send_messages([self])
import dbus
from populous.messaging.concierge.connection import setup_dbus
from populous.messaging.concierge.exceptions import ConciergeError

class PurpleAccount(object):
    def __init__(self, purple, account, *args, **kwargs):
        super(PurpleAccount, self).__init__()
        self.purple = purple
        self._account = account
        
        # Properties
        self.username = unicode(purple.PurpleAccountGetUsername(account))
        self.password = unicode(purple.PurpleAccountGetPassword(account))
        self.protocol = unicode(purple.PurpleAccountGetProtocolName(account))
        self.protocol_id = unicode(purple.PurpleAccountGetProtocolId(account))
    
    def __str__(self):
        return "%s: %s" % (self.protocol, self.username)
    
    def __repr__(self):
        return self.__str__()
    
    def _lookup(self, method):
        attr_cache = '__%s_cache' % method
        if not hasattr(self, attr_cache):
            attr = getattr(self.purple, method)(self._account)
            setattr(self, attr_cache, attr)
        return getattr(self, attr_cache)
        

class PurpleClient(object):
    """
    Python interface to libpurple via dbus.  Woo!
    """
    def __init__(self):
        setup_dbus() # This properly sets the `DBUS_SESSION_BUS_ADDRESS` environ variable so that dbus will work
        try:
            # Try to connect to the concierge daemon via dbus
            self.bus = dbus.SessionBus()
            self.obj = self.bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
            self.purple = dbus.Interface(self.obj, "im.pidgin.purple.PurpleInterface")
        except:
            raise ConciergeError('Could not connect to concierge daemon.  Is it running?')
        
        if self.purple:
            self.accounts = [PurpleAccount(self.purple, account) for account in self.purple.PurpleAccountsGetAll()]
    
    def get_protocol(self, protocol):
        """
        Returns the ``PurpleAccount`` matching the requested ``protocol``.
        Returns `None` if a matching account cannot be found.
        """
        for account in self.accounts:
            if account.protocol == protocol:
                return account
        return None
    
    def send_im(self, protocol, recipient, message):
        """
        Sends an instant ``message`` to ``recipient`` who is on the provided
        ``protocol``.
        
        Returns `True` if the message could be sent, `False` otherwise.
        """
        account = self.get_protocol(protocol)
        if account:
            conv = self.purple.PurpleFindConversationWithAccount(1, recipient, account._account)
            if not conv:
                conv = self.purple.PurpleConversationNew(1, account._account, recipient)
            
            im = self.purple.PurpleConvIm(conv)
            self.purple.PurpleConvImSend(im, message)
            return True
        
        return False
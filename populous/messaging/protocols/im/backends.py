"""
The two backends used by the instant messaging system.  ``DBusBackend``
is used for communicating with a locally running concierge daemon.
Conversely, ``XMLRPCBackend`` is used to communicate with a remote
concierge daemon.

Modify the ``IM_BACKEND`` settings in your settings.py file to let the
system know where the concierge daemon is running.  See the docs for more
info.
"""

class DBusBackend(object):
    def get_protocols(self):
        pass
    
    def send(self, fail_silently=True):
        pass

class XMLRPCBackend(object):
    def get_protocols(self):
        pass
    
    def send(self, fail_silently=True):
        pass
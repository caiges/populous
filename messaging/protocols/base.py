class BaseMessage(object):
    def get_connection(self, fail_silently=False):
        raise NotImplementedError
    
    def message(self):
        """
        Returns a `dictionary` that represent the message.
        
        Should include at least the following keys:
            * `From` - a `string` of the sender
            * `To` - a `string` of the recipient
            * `Date` - a `DateTime`, usually now
            * `Body` - a `string` of the message body
        """
        raise NotImplementedError
    
    def recipients(self):
        """Returns a list of all recipients of the ``Message``."""
        raise NotImplementedError
    
    def send(self, fail_silently=False):
        """Sends the message."""
        raise NotImplementedError
    
    def attach(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted (useful for multipart/alternative messages) and the mimetype
        is guessed, if not provided.
        """
        raise NotImplementedError
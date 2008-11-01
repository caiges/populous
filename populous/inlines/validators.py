from xml.dom import minidom

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class InlineValidator(object):
    """
    Parses a string of XML data and validates all inline elements of the form::
    
        <inline type="inline_name" attr1="attribute 1" />
    
    If you pass ``validate=True`` the validation will occure at instantiation.
    """
    def __init__(self, data, validate=False):
        self.data = data
        self.inlines = self.parse()
        
        if validate:
            self.validate()
    
    def parse(self):
        """
        Parses the xml data and returns ``<inline ... />`` XML nodes.
        
        *Note* the XML data is assumed to be valid, so make sure that it is
        before calling this.
        """
        dom = minidom.parse(StringIO(self.data))
        return dom.getElementsByTagName("inline")
    
    def validate(self):
        for inline in self.inlines:
            # TODO: Get inline class
            try:
                # TODO: Validate inline
                pass
            except:
                raise validators.ValidationError, e
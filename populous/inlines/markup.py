from lxml import etree
from django.utils.safestring import mark_safe
from populous.inlines.utils import get_inline


data = """
<content>
  <h3>Some Header</h3>
  <p>Body text...blah blah blah...</p>
  <inline type="inlines.TemplateInline" template="template.html" />
</content>
"""

class XMLToXHTMLParser(object):
    """
    Converts XML to XHTML.  If you are using your own
    RelaxNG schema, you should probably make a custom
    parser to go along with it.
    
    TODO: Figure out the best way to support this...
    """
    def __init__(self, request, obj, field):
        self.request = request
        self.obj = obj
        self.field = field
        self.output = []
    
    def start(self, tag, attrs):
        if tag == "content":
            return
        elif tag == "inline":
            #TODO: process inlines
            inline = get_inline(*attrs.get('type').split("."))
            self.output.append("<!-- inline goes here (%s) -->" % inline.verbose_name)
            return
        self.output.append("<%s>" % tag)
    
    def end(self, tag):
        if tag == "content":
            return
        elif tag == "inline":
            return
        self.output.append("</%s>" % tag)
    
    def data(self, data):
        self.output.append(data)    
    
    def close(self):
        return self.output

def xml_to_xhtml(data, request, obj, field):
    # TODO: The field should be used to lookup the proper parser
    # for now we'll just use the default XMLToXHTMLParser
    parser = etree.XMLParser(target=XMLToXHTMLParser(request, obj, field))
    result = etree.XML(data, parser)
    return mark_safe("".join(result))
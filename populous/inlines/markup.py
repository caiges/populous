from lxml import etree
from populous.inlines.utils import get_inline

data = """
<content>
  <h3>Some Header</h3>
  <p>Body text...blah blah blah...</p>
  <inline type="inlines.template" template="template.html" />
</content>
"""

class XMLToXHTMLParser(object):
    """
    Converts XML to XHTML.  If you are using your own
    RelaxNG schema, you should probably make a custom
    parser to go along with it.
    
    TODO: Figure out the best way to support this...
    """
    def __init__(self):
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

parser = etree.XMLParser(target=XMLToXHTMLParser())
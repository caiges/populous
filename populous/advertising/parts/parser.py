"""
Classifieds AdPro XML Parser
"""
import re
from xml.dom import minidom

BLANK_PARAGRAPH_RE = re.compile(u'<p style="(?:[\S ]+)">([\s ]+)</p>', re.DOTALL)
SECTION_NAME_RE=re.compile(r'[\d]+<\\#13>@2:([\S ]+)<\\#13>@3:.')

class Paragraph(object):
    def __init__(self, el, ad):
        self._el = el
        self._ad = ad
        self.style = el.attributes.get('style').firstChild.data
        self.text = self.parse_paragraph(el)
    
    def parse_paragraph(self, paragraph):
        """
        Parses ``paragraph``, which should be a minidom ``DOM Element``,
        and returns a properly formatted paragraph string.
        """
        paragraph_str = ''
        for run in paragraph.getElementsByTagName('run'):
            try:
                text = run.firstChild.data
                if text:
                    paragraph_str += run.firstChild.data.replace(u'\xa0', u'')
            except AttributeError:
                continue
        if paragraph_str:
            _paragraph_str = paragraph_str
            paragraph_str = '''<p style="%s">%s</p>''' % (self.style, paragraph_str.strip())
            blank_paragraph = BLANK_PARAGRAPH_RE.match(paragraph_str)
            if not blank_paragraph:
                if len(self._ad.paragraphs) == 0:
                    self._ad.name = _paragraph_str[:50].encode('utf-8', 'ignore')
                self._ad.paragraphs.append(self)
            else:
                print paragraph_str
        return paragraph_str.encode('utf-8', 'ignore')
    
    def __repr__(self):
        return "Paragraph"

class Ad(object):
    def __init__(self, el):
        self._el = el
        self.id = el.attributes.get('id').firstChild.data
        self.paragraphs = []
        self.name = ''
    
    def __repr__(self):
        return "Ad %d" % int(self.id)
    
    def _get_text(self):
        ad_str = ''
        for paragraph in self.paragraphs:
            ad_str += paragraph.text
        return ad_str
    
    text = property(_get_text)

class Section(object):
    def __init__(self, el):
        self._el = el
        self.name = SECTION_NAME_RE.match(el.attributes.get('name').firstChild.data).groups()[0]
        self.callnumber = el.attributes.get('code').firstChild.data
        self.ads = []
    
    def __repr__(self):
        return self.callnumber

def xml_parser(file):
    """
    Parses ``file``, which should be the path to an xml file, and returns
    a `list` of ``Section`` objects.
    """
    section_list = []
    dom = minidom.parse(file)
    classifieds = dom.getElementsByTagName('classifieds')[0]
    sections = classifieds.getElementsByTagName('section')
    for s in sections:
        section = Section(s)
        section_list.append(section)
        for a in s.getElementsByTagName('ad'):
            ad = Ad(a)
            section.ads.append(ad)
            for p in a.getElementsByTagName('paragraph'):
                paragraph = Paragraph(p, ad)
    return section_list
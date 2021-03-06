from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.forms.util import ValidationError as FormsValidationError
from django.utils.encoding import smart_unicode
from django.template.defaultfilters import truncatewords_html

from lxml import etree
import re

# Can't use cStringIO because it messes up the unicode string
from StringIO import StringIO

class RelaxNGValidator(object):
    "Validate against a Relax NG schema"
    def __init__(self, schema_path, additional_root_element=None):
        self.schema_path = schema_path
        self.additional_root_element = additional_root_element
    
    def raiseValidationError(self, xml_data, error_log):
        display_errors = []
        if self.additional_root_element:
            adjust_line = -1
        else:
            adjust_line = 0
        lines = xml_data.split('\n')
        for error in error_log:
            # Scrape the lxml error messages to reword them more nicely.
            m = re.search(r'Opening and ending tag mismatch: (.+?) line (\d+?) and (.+?)$', error.message)
            if m:
                display_errors.append(_(u'Please close the unclosed %(tag)s tag from line %(line)s. (Line starts with "%(start)s".)') % \
                    {'tag':m.group(1).replace('/', ''), 'line':int(m.group(2)) + adjust_line, 'start':lines[int(m.group(2)) - 1][:30]})
                continue
            m = re.search(r'Did not expect text in element (.+?) content', error.message)
            if m:
                display_errors.append(_(u'Some text starting on line %(line)s is not allowed in that context. (Line starts with "%(start)s".)') % \
                    {'line':error.line + adjust_line, 'start':lines[int(error.line) - 1][:30]})
                continue
            m = re.search(r'Specification mandate value for attribute (.+?)$', error.message)
            if m:
                display_errors.append(_(u'"%(attr)s" on line %(line)s is an invalid attribute. (Line starts with "%(start)s".)') % \
                    {'attr':m.group(1), 'line':error.line + adjust_line, 'start':lines[int(error.line) - 1][:30]})
                continue
            m = re.search(r'Invalid attribute (.+?) for element (.+?)$', error.message)
            if m:
                display_errors.append(_(u'"%(attr)s" on line %(line)s is an invalid attribute. (Line starts with "%(start)s".)') % \
                    {'attr':m.group(1), 'line':error.line + adjust_line, 'start':lines[int(error.line) - 1][:30]})
                continue
            m = re.search(r'Did not expect element (.+?) there', error.message)
            if m:
                display_errors.append(_(u'"<%(tag)s>" on line %(line)s is an invalid tag. (Line starts with "%(start)s".)') % \
                    {'tag':m.group(1), 'line':error.line + adjust_line, 'start':lines[int(error.line) - 1][:30]})
                continue
            m = re.search(r'Element (.+?) failed to validate attributes', error.message)
            if m:
                display_errors.append(_(u'A tag on line %(line)s is missing one or more required attributes. (Line starts with "%(start)s".)') % \
                    {'line':error.line + adjust_line, 'start':truncatewords_html(lines[int(error.line) - 1], 5)})
                continue
            m = re.search(r'Invalid attribute (.+?) for element (.+?)$', error.message)
            if m:
                display_errors.append(_(u'The "%(attr)s" attribute on line %(line)s has an invalid value. (Line starts with "%(start)s".)') % \
                    {'attr':m.group(1), 'line':error.line + adjust_line, 'start':lines[int(error.line) - 1][:30]})
                continue
            # Failing all those checks, use the default error message.
            display_errors.append(u'Line %s: %s [%s]' % (error.line + adjust_line, error.message, error.level_name))
        raise ValidationError, display_errors
    
    def validate(self, xml_data):
        self.errors = []
        if self.additional_root_element:
            xml_data = u'<%(are)s>\n%(data)s\n</%(are)s>' % {
                'are': self.additional_root_element,
                'data': xml_data
            }
        
        etree.clear_error_log()
        try:
            doc = etree.parse(StringIO(xml_data))
        except etree.XMLSyntaxError, e:
            self.raiseValidationError(xml_data, e.error_log)
        etree.clear_error_log()
        
        schema_path = self.schema_path
        if schema_path:
            if not schema_path[0] == '/':
                import os.path
                schema_path = os.path.join(os.path.dirname(__file__), "rng/%s" % schema_path)
            
            try:
                rng_doc = etree.parse(schema_path)
                rng = etree.RelaxNG(rng_doc)
            except (etree.XMLSyntaxError, etree.RelaxNGParseError), e:
                import os.path
                raise ValidationError, [_(u"Could not load %s for validation, please contact the admin") % os.path.basename(self.schema_path)]
            if not rng(doc):
                self.raiseValidationError(xml_data, rng.error_log)
    
    # oldforms-way of using this
    def __call__(self, field_data, all_data):
        from django.core.validators import ValidationError as CoreValidationError
        try:
            self.validate(field_data)
        except ValidationError, e:
            raise CoreValidationError(e)
    
    # newforms-way of using this
    def forms_validate(self, value):
        try:
            self.validate(value)
        except ValidationError, e:
            raise FormsValidationError(e[0])    #TODO: This seems odd...but seems to work--verify
        return smart_unicode(value)
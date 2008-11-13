from django.contrib.admin.widgets import AdminTextareaWidget, ForeignKeyRawIdWidget as DefaultForeignKeyRawIdWidget
from django.forms.widgets import Textarea
from django.db.models.fields.related import ManyToOneRel
from django.utils.safestring import mark_safe
from django.template import loader, Context, Template
from django.conf import settings
#from populous.inlines.markup import xml_to_editor
from xml.dom import minidom

from populous.inlines.utils import unicode_to_html

class ForeignKeyRawIdWidget(DefaultForeignKeyRawIdWidget):
    """
    This behaves just like django.contrib.auth's ForeignKeyRawIdWidget, however,
    it takes a Django model as a required argument.  It also accepts a
    limit_choices_to argument, which behaves indentically as defined in the
    Django models documentation.
    """
    def __init__(self, model, limit_choices_to=None, attrs=None):
        rel = ManyToOneRel(model, model._meta.pk.name, limit_choices_to=limit_choices_to)
        super(ForeignKeyRawIdWidget,self).__init__(rel, attrs)


class InlineTextareaWidget(Textarea):
    """
    Adds the required javascript for use with ``InlineField``.
    """
    
    class Media:
        js = (
            '/admin_media/tinymce_2/jscripts/tiny_mce/tiny_mce.js',
            '/admin_media/tinymce_setup/inlines_setup.js'
        )
    
    def render(self, name, value, attrs=None):
        from populous.inlines.models import RegisteredInline
        
        t = loader.select_template([
            'inlines/widgets/inline_textarea_%s.html' % name,
            'inlines/widgets/inline_textarea.html'
        ])
        
        #value = value.rstrip('</content>').lstrip('<content>')
        if value:
            try:
                dom = minidom.parseString(value)
                value = unicode_to_html(''.join([n.toxml() for n in dom.firstChild.childNodes]))
            except:
                pass
        default = super(InlineTextareaWidget, self).render(name, value, attrs)
        
        inline_js = loader.get_template('inlines/parts/inline.js')
        c = Context({
            'MEDIA_URL': settings.MEDIA_URL,
            'name': name,
            'value': value,
            'attrs': attrs,
            'default': default,
            #'inlines': mark_safe('[%s]') % ','.join([inline_js.render(Context({'inline': inline})) for inline in RegisteredInline.objects.all()])
        })
        return mark_safe(t.render(c))
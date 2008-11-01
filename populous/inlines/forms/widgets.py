from django.contrib.admin.widgets import AdminTextareaWidget, ForeignKeyRawIdWidget as DefaultForeignKeyRawIdWidget
from django.forms.widgets import Textarea
from django.db.models.fields.related import ManyToOneRel
from django.utils.safestring import mark_safe
from django.template import loader, Context, Template
from django.conf import settings

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


INLINE_TEMPLATE = Template(mark_safe("""{
    name: "{{ inline.name }}",
    className: "{{ inline.class_name }}",
    replaceWith: function() {
        var data;
        $.ajax({
            async: false,
            type: "GET",
            url: "{{ inline.get_form_url }}",
            success: function(html){
                data = html;
            }
        });
        return data;
    }
}"""))


class InlineTextareaWidget(Textarea):
    """
    Adds the required javascript for use with ``InlineField``.
    """
    
    class Media:
        css = {
            'all': (
                "%sinlines/markitup/skins/simple/style.css" % settings.MEDIA_URL, 
                "%sinlines/markitup/sets/newsml/style.css" % settings.MEDIA_URL,)
        }
        
        js = (
            "%sinlines/markitup/jquery.markitup.js" % settings.MEDIA_URL,
            "%sinlines/markitup/sets/newsml/set.js" % settings.MEDIA_URL,
            )
    
    def render(self, name, value, attrs=None):
        from populous.inlines.models import RegisteredInline
        
        t = loader.select_template([
            'inlines/widgets/inline_textarea_%s.html' % name,
            'inlines/widgets/inline_textarea.html'
        ])
        
        inline_js = loader.get_template('inlines/parts/inline.js')
        c = Context({
            'MEDIA_URL': settings.MEDIA_URL,
            'name': name,
            'value': value,
            'attrs': attrs,
            'default': super(InlineTextareaWidget, self).render(name, value, attrs),
            'inlines': mark_safe('[%s]') % ','.join([inline_js.render(Context({'inline': inline})) for inline in RegisteredInline.objects.all()])
        })
        return mark_safe(t.render(c))
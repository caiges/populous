"""
Default included Inline subclasses.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.template import loader, RequestContext
from populous.inlines.base import Inline
from populous.inlines.forms import InlineForm


class TextInlineForm(InlineForm):
    title = forms.CharField(label=_("Title"), required=False)
    content = forms.CharField(label=_("Content"), widget=forms.Textarea)
    template = forms.CharField(label=_("Template"), required=False)

class TextInline(Inline):
    """
    A simple inline that stores text.  A custom form can be defined as well. 
    """
    verbose_name = _('text box')
    verbose_name_plural = _('text boxes')
    form = TextInlineForm

    def render(self, request, obj, field):
        app_label, module_name = obj._meta.app_label, obj._meta.module_name
        print app_label, module_name
        t = loader.select_template([
            self.data.get('template'),
            "inlines/textinline/%s/%s_%s_%s.html" % (app_label, module_name, obj.pk, field.name),
            "inlines/textinline/%s/%s_%s.html" % (app_label, module_name, obj.pk),
            "inlines/textinline/%s/%s.html" % (app_label, module_name),
            "inlines/textinline/default.html"
        ])
        c = RequestContext(request, {
            'inline': self,
            'obj': obj})
        return t.render(c)


class TemplateInlineForm(InlineForm):
    template = forms.CharField(label=_("Template"))
        
class TemplateInline(Inline):
    """
    An inline that doesn't have any content, but will include a template specific
    to the content_type of the object that is including it.  Templates rendered by
    this inline will get rendered in the same context at the referencing object.
    """
    verbose_name = _('template')
    form = TemplateInlineForm
    # TODO: think more about this one.


class GenericModelInlineForm(InlineForm):
    #content_type = forms.ModelChoiceField
    #object_id = forms.IntegerField()
    pass

class GenericModelInline(Inline):
    """
    A ``GenericModelInline`` is an inline that uses Django's `contenttypes` contrib
    application.  This allows...
    """
    verbose_name = _('generic model')
    form = GenericModelInlineForm


class ReverseInlineForm(InlineForm):
    pass

class ReverseInline(Inline):
    verbose_name = _('reverse inline')
    form = ReverseInlineForm
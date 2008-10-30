"""
Default included Inline subclasses.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
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
    default_template = 'inlines/textinline.html'
    verbose_name = _('text box')
    verbose_name_plural = _('text boxes')
    form = TextInlineForm


class TemplateInlineForm(InlineForm):
    template = forms.CharField(label=_("Template"), required=False)
        
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
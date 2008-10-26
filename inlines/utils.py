from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass
from django.contrib.markup.templatetags.markup import restructuredtext

def form_from_fields(name, form=forms.Form, fields={}):
    """
    Returns a forms.Form class with a name, `name`, a Form baseclass, `form`, and
    a dictionary of fields, `fields`.
    """
    return DeclarativeFieldsMetaclass(name, (form,), fields)

def get_inline_description(inline):
    """
    Returns a string that has been converted from
    ``restructuredtext`` into HTML.
    
    TODO: The output is kinda wonky
    """
    text = getattr(inline, '__doc__', '')
    if text is None:
        return ''
    return restructuredtext(text.strip())
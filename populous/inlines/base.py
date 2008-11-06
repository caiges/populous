import sys
from django import forms
from django.utils.translation import string_concat
from django.core.exceptions import ImproperlyConfigured
from django.db.models.options import get_verbose_name
from django.utils.text import capfirst

from populous.inlines.forms import InlineForm, ForeignKeyRawIdWidget
from populous.inlines.utils import form_from_fields

def build_name(name):
    names = []
    out_names = []
    i = -1
    for char in name:
        if char.isupper():
            i += 1
            names.append("")
        names[i] += char.lower()
    
    for name_bit in names:
        if name_bit.find("inline") < 0:
            out_names.append(name_bit)
    return "_".join(out_names)

class InlineMetaclass(type):
    """
    Metaclass for ``Inline`` subclasses.  The reason that we use this metaclass
    is so that the attributes assigned to an ``Inline`` get calculated at the
    moment the class is contructed, rather than waiting untill it is instantiated.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(InlineMetaclass, cls).__new__
        new_class = super_new(cls, name, bases, attrs)
        
        # TODO: This is super hacky...
        if new_class.__name__ not in ("Inline", "ModelInline"):
            inline_module = sys.modules[cls.__module__]
            new_class.app_label = inline_module.__name__.split('.')[-2]
            for base in bases[::-1]:
                if not new_class.name:
                    new_class.name = build_name(new_class.__name__)
                else:
                    new_class.name = new_class.name.lower()
                    if new_class.name.find(" "): #TODO make this better
                        raise ImproperlyConfigured, "Spaces are not allowed in inline names: %s." % new_class.name
                            
                new_class.verbose_name = getattr(base, 'verbose_name', None) or new_class.name
                new_class.verbose_name_plural = getattr(base, 'verbose_name_plural', None) or \
                                                string_concat(new_class.verbose_name, 's')
                new_class.display_group = getattr(base, 'display_group', None) or getattr(base, 'app_label', None)
            
            cls.check_form(new_class)
            
        return new_class
    
    def check_form(new_class):
        if new_class.form is None:
            raise ImproperlyConfigured, 'You must define a form attribute for %s.' % new_class.__name__
    
class Inline(object):
    """
    Functionality common to all inline subclasses.
    """
    __metaclass__ = InlineMetaclass
    
    verbose_name = None
    verbose_name_plural = None  # Calculated automatically
    display_group = None        # A string which denotes how to group this inline with other inlines.  Defaults to app_label
    form = None                 # The InlineForm class which can be used to create a valid inline instance
    default_template = None     # The default template used when render() is called on this inline's instance
    app_label = None            # Conputed automatically based on location in codebase (same method as Django uses for models)
    name = None                 # This must be unique per app
    
    def __init__(self):
        pass
    
    
    def validate(self, attrs, content):
        """
        
        """
        return True
    
    def render(self, request, obj, attrs, content, **kwargs):
        pass


class ModelInlineMetaclass(InlineMetaclass):
    def __new__(cls, name, bases, attrs):
        from django.db.models import get_model
        new_class = super(ModelInlineMetaclass, cls).__new__(cls, name, bases, attrs)
        
        if new_class.__name__ != "ModelInline":
            new_class.model = new_class.model or get_model(new_class.app_label, new_class.model)
            
            if new_class.form is None:
                new_class.form = cls._create_form(new_class)
        
        return new_class
    
    def check_form(new_class):
        return True
    
    def _create_form(new_class):
        """
        Returns a subclass of ``InlineForm`` that is bound to a model
        specified by ``cls.model``.
        """
        defaults = {'label': capfirst(new_class.model._meta.verbose_name)}
        if new_class.raw_id_admin:
            formfield = forms.CharField
            if new_class.limit_choices_to is None:
                defaults['widget'] = ForeignKeyRawIdWidget(new_class.model)
            else:
                defaults['widget'] = ForeignKetRawIdWidget(new_class.model, new_class.limit_choices_to)
        else:
            formfield = forms.ModelChoiceField
            if new_class.limit_choices_to is None:
                # limit_choices_to is not defined, so get all objects
                defaults['queryset'] = new_class.model._default_manager.all()
            else:
                defaults['queryset'] = new_class.model._default_manager.complex_filter(new_class.limit_choices_to)
        return form_from_fields(new_class.model.__name__ + 'InlineModelForm', InlineForm,
                                                                {new_class.model.__name__.lower(): formfield(**defaults)})
        

class ModelInline(Inline):
    """
    A base class for inlines that display a Django model.  Subclasses should
    define at least one attribute, `model`, which should be a valid Django
    model (not an instance).
    """
    __metaclass__ = ModelInlineMetaclass
    
    raw_id_admin = True         # If True then the auto generated AdminForm will use a special widget
    limit_choices_to = None     # Works just like in Django's model decumentation
    model = None                # Model class or string
    
    def render(self, request, obj, attrs, content, **kwargs):
        # TODO: write this
        pass
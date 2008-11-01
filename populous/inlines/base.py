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
    
class Inline(object):
    """
    Functionality common to all inline subclasses.
    """
    
    verbose_name = None
    verbose_name_plural = None  # Calculated automatically
    display_group = None        # A string which denotes how to group this inline with other inlines.  Defaults to app_label
    form = None                 # The Form class which can be used to create a valid inline instance
    default_template = None     # The default template used when render() is called on this inline's instance
    app_label = None            # Conputed automatically based on location in codebase (same method as Django uses for models)
    name = None                 # This must be unique per app
    
    def __init__(self):        
        inline_class = self.__class__
        inline_module = sys.modules[inline_class.__module__]
        self.app_label = inline_module.__name__.split('.')[-2]
        
        if not self.name:
            self.name = build_name(inline_class.__name__)
        else:
            self.name = self.name.lower()
            if self.name.find(" "): #TODO make this better
                raise ImproperlyConfigured, "Spaces are not allowed in inline names: %s." % self.name
        
        self.verbose_name = self.verbose_name or get_verbose_name(inline_class.__name__)
        self.verbose_name_plural = self.verbose_name_plural or string_concat(self.verbose_name, 's')
        self.display_group = self.display_group or self.app_label
    
    def get_form(self, request, content_type, field, obj_id=None):
        """
        Subclasses can override this to provide more customized form options.  In the default
        case, we just want to raise an exception if no form is provided.
        
        The form returned will be used to build the inline markup, which looks something like this::
        
            <inline type="inline_name" attr1="attribute 1", attr2="attribute 2" />
        
        ``inline_name`` is the ``name`` of the inline, and everything else are form field values.
        """
        if self.form is None:
            raise ImproperlyConfigured, 'You must define a form attribute for %s.' % self.__class__.__name__
        return self.form
    
    def validate(self, attrs, content):
        pass
    
    def render(self, obj, attrs, content, **kwargs):
        pass

class ModelInline(Inline):
    """
    A base class for inlines that display a Django model.  Subclasses should
    define at least one attribute, `model`, which should be a valid Django
    model (not an instance).
    """
    raw_id_admin = True         # If True then the auto generated AdminForm will use a special widget
    limit_choices_to = None     # Works just like in Django's model decumentation
    model = None                # Model class or string
    
    def __init__(self):
        from django.db.models import get_model
        self.model = self.model or get_model(self.app_label, self.model)
        super(ModelInline, self).__init__()
    
    def get_form(self, request, content_type, field, obj_id=None):
        """
        Custom method override which creates a sane default form.
        """
        if self.form is None:
            defaults = {'label': capfirst(self.model._meta.verbose_name)}
            if self.raw_id_admin:
                formfield = forms.CharField
                if self.limit_choices_to is None:
                    defaults['widget'] = ForeignKeyRawIdWidget(self.model)
                else:
                    defaults['widget'] = ForeignKetRawIdWidget(self.model, self.limit_choices_to)
            else:
                formfield = forms.ModelChoiceField
                if self.limit_choices_to is None:
                    # limit_choices_to is not defined, so get all objects
                    defaults['queryset'] = self.model._default_manager.all()
                else:
                    defaults['queryset'] = self.model._default_manager.complex_filter(self.limit_choices_to)
            self.form = form_from_fields(self.model.__name__ + 'InlineModelForm', InlineForm,
                                                                    {self.model.__name__.lower(): formfield(**defaults)})
    
    def render(self):
        # TODO: write this
        pass
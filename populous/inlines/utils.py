import sys
import os
from xml.dom import minidom

from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass
from django.contrib.markup.templatetags.markup import restructuredtext
from django.template import loader, Context
from django.conf import settings

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
    
    TODO: The output is kinda wonky (needs html to be reformatted)
    """
    text = getattr(inline, '__doc__', '')
    if text is None:
        return ''
    return restructuredtext(text.strip())

def get_absolute_schema_path(path):
    """
    Returns the absolute schema path.
    
    TODO: This could probably use some cleanup...
    """
    if path[0] == "/":
        # Assume this is an absolute path
        return path
    
    # Since this isn't an absolute path, we want to try to look
    # in a user-defined location first
    if hasattr(settings, "INLINES_SCHEMA_PATH"):
        path_prefix = getattr(settings, "INLINES_SCHEMA_PATH")
    else:
        # Since the user has not defined a specific location, we
        # will now look under the project directory for a `schemas`
        # directory
        project_mod_name = os.getenv('DJANGO_SETTINGS_MODULE').split('.')[0]
        project_dir = sys.modules[project_mod_name].__path__[0]
        path_prefix = "%s/schemas/" % project_dir

    return "%s%s" % (path_prefix, path)

class Schema(object):
    """
    A class for creating and writing RelaxNG schemas.
    """
    def __init__(self, base_schema, output_schema):
        self.base_schema = base_schema
        self.output_schema = output_schema
    
    def _open(self, name, filemode, dirmode=0777):
        """
        Attempts to return an open file and try to create all intermediate
        directories.
        """
        try:
            return open(name, filemode)
        except IOError, e:
           if e[0] != 2: # didn't work for some other reason
               raise e
           lastsep = name.rfind(os.sep)
           if lastsep == -1:
               raise
           os.makedirs(name[:lastsep], dirmode)
           return open(name, filemode)
    
    def generate_schema(self):
        from populous.inlines.models import RegisteredInline
        t = loader.get_template("inlines/schemas/%s" % self.base_schema)
        c = Context({
            'inline_list':  RegisteredInline.objects.all()
        })
        self.generated_schema = t.render(c)
    
    def write(self):
        output_dir = getattr(settings, "INLINES_SCHEMA_DIR", "schemas").rstrip("/")
        if output_dir[0] != "/":
            # This is a relative path, so look for the directory relative to the project directory
            project_mod_name = os.getenv('DJANGO_SETTINGS_MODULE').split('.')[0]
            project_dir = sys.modules[project_mod_name].__path__[0]
            output_dir = "%s/%s" % (project_dir, output_dir)

        # Now that output_dir is an absolute path, tack on the output file name and open the file for writing
        output_path = "%s/%s" % (output_dir, self.output_schema)
        schema_file = self._open(output_path, 'w')
        
        if not hasattr(self, 'generated_schema'):
            # No call has been made to ``generate_schema``, so do it now
            self.generate_schema()
        
        schema_file.write(self.generated_schema)
        schema_file.close()
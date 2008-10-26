from populous.inlines.base import Inline, ModelInline
from populous.inlines.forms import InlineForm, ForeignKeyRawIdWidget
from populous.inlines.models import RegisteredInline, RegisteredInlineField
from populous.inlines.fields import InlineField

__all__ = ['Inline', 'ModelInline', 'InlineForm', 'ForeignKeyRawIdWidget',
            'RegisteredInline', 'RegisteredInlineField', 'InlineField']

from django.db.models.signals import post_syncdb
from populous.inlines.management.commands.inlines import Command

def sync_inlines(sender, **kwargs):
    verbosity = kwargs.get('verbosity', 2)
    c = Command()
    if verbosity > 1:
        c.verbose = True
    else:
        c.verbose = False
    c.sync([sender])

post_syncdb.connect(sync_inlines)
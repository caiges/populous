from django.core.management.base import BaseCommand, CommandError
from populous.inlines.base import Inline
from populous.inlines.fields import InlineField
from populous.inlines.models import RegisteredInline, RegisteredInlineField

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list
    allowed_args = ['sync', 'reset']
    help = 'Management commands for the Inlines app.'
    args = '%s [appname ...]' % "|".join(allowed_args)
    
    def handle(self, *args, **options):
        from django.db.models import get_apps, get_app
        
        self.verbose = options.get('verbose', False)
        
        if len(args) > 0:
            command, app_list = args[0].lower(), args[1:]
            
            if len(app_list) == 0:
                app_list = get_apps()
            else:
                app_list = [get_app(app) for app in app_list]
            
            if command not in self.allowed_args:
                raise CommandError("The first argument passed should one of the following: %s" \
                                                        % ", ".join(self.allowed_args))            
            if command == "sync":
                self.sync(app_list)
            elif command == "reset":
                self.reset(app_list)
    
    def reset(self, app_list):
        pass
    
    def imp_inline_mod(self, app_name):
        """
        This will return the inlines module for a given app.
        For example, if ``app_name`` is `populous.inlines',
        then this will attempt to import `populous.inlines.inlines`.
        """
        name = "%s.inlines" % app_name
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    
    def sync(self, app_list):
        from django.db.models import get_models, get_app
                        
        for app in app_list:
            #app = get_app(app_name.split('.')[-1])
            app_name = app.__name__.rsplit('.', 1)[0]
            try:
                mod = self.imp_inline_mod(app_name)
                for item in [item for item in dir(mod) if not item.startswith('_')]:
                    item = getattr(mod, item)
                    if mod.__name__ == getattr(item, '__module__', '') and issubclass(item, Inline):
                        # This is a subclass of Inline, so add it to the cache
                        inline = item()                            
                        reged_inline, created = RegisteredInline.objects.create_from_inline(inline)
                        
                        if self.verbose:
                            print "Found Inline subclass, `%s`, in `%s`" % (item.__name__, mod.__name__)
                            if not created:
                                print "\tInline already exists; skipping addition."
                            else:
                                print "\tInline doesn't exist yet; adding it."
            except ImportError:
                # This app doesn't have any inlines
                if self.verbose:
                    print "App `%s` doesn't have any inlines" % app_name
        
            for model in get_models(app):
                for field in model._meta.fields:
                    if isinstance(field, InlineField):
                        obj, created = RegisteredInlineField.objects.create_from_field(model, field)
                        if self.verbose:
                            print "Found `InlineField` in model `%s`" % model.__name__
                            if not created:
                                print "\tField already exists; skipping addition."
                            else:
                                print "\tField doesn't exist yet; adding it."
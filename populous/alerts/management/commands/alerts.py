from django.core.management.base import BaseCommand, CommandError, make_option
from populous.alerts.models import Subscription

class Command(BaseCommand):
    option_list = list(BaseCommand.option_list)
    option_list.append(
        make_option('-s', '--fail_silently', action='store_true',
            help='Fail siliently instead of making a bunch of noise.')
    )
    can_import_settings = True
    args = ['send',]
    help = 'Management commands for the alerts app.'
    
    def handle(self, *args, **options):
        self.verbose = options.get('verbose', False)
        fail_silently = options.get('fail_silently', False)

        if len(args) > 0:
            command = args[0].lower()
            
            if command == "send":
                Subscription.objects.send_due(fail_silently)
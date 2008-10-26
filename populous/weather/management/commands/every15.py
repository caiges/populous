from django.core.management.base import BaseCommand, CommandError
from weather.utils import location

class Command(BaseCommand):
    help = "Updates the current forecast. Run as often as necessary."
    def handle(self, *args, **options):
        location.get_current(location.get_location())

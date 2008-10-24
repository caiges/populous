from django.core.management.base import BaseCommand, CommandError
from weather.utils import location 

class Command(BaseCommand):
    help = "Updates the long range forecasts. Run daily."
    def handle(self, *args, **options):
        location.get_forecast(location.get_location())

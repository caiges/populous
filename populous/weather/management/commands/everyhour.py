from django.core.management.base import BaseCommand, CommandError
from weather.utils import location

class Command(BaseCommand):
    help = "Gets the more details forecast with icons. Run hourly"
    def handle(self, *args, **options):
        location.get_hourly(location.get_location())

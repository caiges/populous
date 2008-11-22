from django.contrib.syndication.feeds import Feed
from populous.locations.models import Location, LocationType

class LocationFeed(Feed):
    title = 'Locations Feed'
    link = '/locations'
    description = 'Locations feed description'
    
    def get_object(self, bits):
        if len(bits) == 1:
            try:
                return LocationType.objects.get(slug__exact=bits[0])
            except LocationType.DoesNotExist:
                raise LocationType.DoesNotExist
        
        return None
    
    def item_link(self):
        return '/'
    
    def items(self, obj):
        if obj is not None:
            return Location.objects.filter(location_type__id=obj.id)[:5]
        
        return Location.objects.all()[:5]

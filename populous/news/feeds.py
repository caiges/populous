from django.contrib.syndication.feeds import Feed
from populous.news.models import Collection

class CollectionFeed(Feed):
    title = 'Collection Feed'
    link = '/collections'
    description = 'Collection feed description'
    
    def get_object(self, bits):
        if len(bits) == 1:
            try:
                return Collection.objects.get(url__exact=bits[0])
            except Collection.DoesNotExist:
                raise Collection.DoesNotExist
        
        return None
    
    def item_link(self):
        return '/'
    
    def items(self, obj):
        if obj is not None:
            return obj.get_collection_objects()
        
        return []

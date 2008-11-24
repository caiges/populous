from django.contrib.syndication import feeds
from populous.news.models import Collection

class CollectionFeed(feeds.Feed):    
    def title(self, obj):
        return u"Latest %s Entries" % obj
    
    def link(self, obj):
        if not obj:
            raise feeds.FeedDoesNotExist
        return obj.get_absolute_url()
    
    def description(self, obj):
        return u"%s updates" % obj
    
    def get_object(self, bits):
        url = u"/%s/" % u"/".join([bit for bit in bits if bit]) # This is my favorite line of code ever :)
        try:
            return Collection.objects.get(url__exact=url)
        except Collection.DoesNotExist:
            raise Collection.DoesNotExist
        return None
    
    def items(self, obj):
        if obj is not None:
            return obj.get_collection_objects()
        return []
    
    def item_pubdate(self, item):
        return item.pub_date
            
from populous.alerts.alerts import AlertForFeed
from populous.news.parts.feeds import CollectionFeed

class CollectionAlert(AlertForFeed):
    feed_class = CollectionFeed

from populous.alerts.alerts import AlertForFeed
from populous.news.feeds import CollectionFeed

class CollectionAlert(AlertForFeed):
    feed_class = CollectionFeed

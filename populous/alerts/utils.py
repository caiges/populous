import rfc822
from cElementTree import iterparse
from urllib import urlopen
from datetime import datetime
from StringIO import StringIO

def build_dt(date):
    time_tuple = rfc822.parsedate_tz(date)
    return datetime(*time_tuple[:7])

def  parse_feed(feed_url, fail_silently):
    items = []
    feed = None
    
    try:
        feed = urlopen(feed_url)
    except IOError, e:
        if not fail_silently:
            raise IOError, e
        pass
    
    if feed is not None:
        for event, elem in iterparse(feed):
            if elem.tag == "item":
                items.append({
                    'title':    elem.findtext("title"),
                    'pub_date': build_dt(elem.findtext("pubDate")),
                    'link':     elem.findtext("link")
                })
                elem.clear()
    return items
from django import template
from django.template import Variable, VariableDoesNotExist
from django.utils.safestring import mark_safe

from topics.models import TopicCollection

register = template.Library()

class TopicCollectionNode(template.Node):
    def __init__(self, num=None, varname='topic_collection'):
        self.limit = num
        self.varname = varname
    
    def render(self, context):
        url = context['request'].META['PATH_INFO']
        prefix_url = url.rstrip('/').rsplit('/', 1)[0]  # Everything but the last bit
        
        # Try the simple case first, exact match
        try:
            print "Trying %s" % url
            collection = TopicCollection.objects.get(url__iexact=url)
        except TopicCollection.DoesNotExist:
            collection = []
            prefix = url
            while prefix:
                prefix = "%s/" % prefix.rstrip('/').rsplit('/', 1)[0]  # Everything but the last bit--need trailing slash too!
                print "Trying %s" % prefix
                try:
                    collection = TopicCollection.objects.get(url__iexact=prefix)
                    print "Found match: %s" % prefix
                    break
                except TopicCollection.DoesNotExist:
                    pass
        
        context[self.varname] = collection
        return ''

@register.tag
def get_topic_collection(parser, token):
    """
    {% get_topic_collection [num] [as varname]%}
    
    Returns the topics associated with the topic collection object with URL that matches the current path best.
    Optional 'num' limits the number of topics from the specified collection.
    """
    bits = token.split_contents()
    if len(bits) == 1:
        return TopicCollectionNode()
    elif len(bits) == 2:
        return TopicCollectionNode(bits[1])
    elif len(bits) == 4:
        return TopicCollectionNode(bits[1], bits[3])
    else:
        raise template.TemplateSyntaxError("%s: Argument takes 0 or 1 arguments" % bits[0])

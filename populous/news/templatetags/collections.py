from django import template
from django.template import Variable, VariableDoesNotExist
from django.utils.safestring import mark_safe

from news.models import Collection

register = template.Library()

class CollectionLatestNode(template.Node):
    def __init__(self, url, limit, varname):
        self.url = url
        self.limit = int(limit)
        self.varname = varname
    
    def render(self, context):
        try:
            collection = Variable(self.url).resolve(context)
        except VariableDoesNotExist:
            collection = None
        try:
            if not collection:
                collection = Collection.objects.get(url=self.url)
            object_list = collection.get_collection_objects()[:self.limit]
            result = []
            for obj in object_list:
                try:
                    obj = obj.content_object
                except AttributeError:
                    pass
                app_label = obj._meta.app_label
                module_name = obj._meta.module_name
                context['object'] = obj
                t = template.loader.select_template(['news/collections/%s/%s_%s_%s.html' % (collection.id, app_label, module_name, obj.id), 'news/collections/%s/%s_%s.html' % (collection.id, app_label, module_name), 'news/collections/%s_%s.html' % (app_label, module_name)])
                response = mark_safe(t.render(context))
                result.append(response)
            context[self.varname] = result
            return ''
        except Exception, e:
            return "<!-- ERROR: %s -->" % e

@register.tag
def get_collection_latest(parser, token):
    """
    {% get_latest_from_collection collection_url num as latest_forecast  %}
    
    Returns the most recent 'num' items from the specified collection.
    """
    bits = token.split_contents()
    if len(bits) == 5:
        return CollectionLatestNode(bits[1], bits[2], bits[4])
    else:
        raise template.TemplateSyntaxError("%s: Argument takes 4 arguments" % bits[0])

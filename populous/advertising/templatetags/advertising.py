from django import template
from django.conf import settings
from populous.advertising.models import ClassifiedAd, ClassifiedSubCategory
from populous.core.parts.templatetags import CachedContextUpdatingNode

register = template.Library()

class PlacementNode(template.Node):
    def __init__(self, id, height, width, template):
        self.id = int(id)
        self.height = int(height)
        self.width = int(width)
        self.template = template
        self.placement = None

    def __unicode__(self):
        return "<PlacementNode>"

    def render(self, context):
        self.ad_url = '''%sadvertising/ad/?placement=%d&template=%s''' % (settings.AD_SERVER, self.id, self.template or "''")
        self.ad_display = 'ad%d' % self.id
        return '''<iframe width="%s" height="%s" scrolling="no" frameborder="no" framespacing="0" src="%s" name="%s" id="%s"></iframe>''' % (
            self.width or "100%",
            self.height or "100%",
            self.ad_url,
            self.ad_display, self.ad_display
        )

def DoGetPlacementFrame(parser, token):
    """
    Usage:
    {% get_placement_frame [id] [height] [width] [template] %}
   
    Outputs the proper <iframe> markup for the advertising placement and optional template.
    """
    bits = token.contents.split()
    if len(bits) == 4:
        return PlacementNode(bits[1], bits[2], bits[3], '')
    elif len(bits) == 5:
        return PlacementNode(bits[1], bits[2], bits[3], bits[4])
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes an integer value of the placement id, height, width and an optional template string" % bits[0]

class RandomClassifiedsNode(CachedContextUpdatingNode):
    def __init__(self, number_ads, varname, cache_timeout):
        self.num_ads = number_ads
        self.varname = varname
        self.cache_timeout = cache_timeout
    
    def __unicode__(self):
        return u"<Top6ClassifiedsNode>"
    
    def get_cache_key(self, context):
        return "populous.advertising.classifieds.templatetags.get_random_classifieds:%s:%s:%s:%s" % (self.varname, self.num_ads, self.cache_timeout, settings.SITE_ID)
    
    def get_content(self, context):
        context[self.varname] = ClassifiedAd.objects.all().order_by('?')[:self.num_ads]

def GetRandomClassifieds(parser, token):
    """
    Gets [number of ads] classified ads ordered randomly taken from all current classified ads.
    A context, either 'random_classified_ad_list' or [varname] item will be added and cached for [cache_timeout] seconds.
    
    Syntax::
    
        {% get_random_classifieds [number of ads] [as varname] [for cache_timeout (in seconds)] %}
    """
    bits = token.contents.split()
    DEFAULT_VARNAME = 'random_classified_ad_list'
    DEFAULT_CACHE_TIMEOUT = 0
    if len(bits) == 2:
        return RandomClassifiedsNode(bits[1], DEFAULT_VARNAME, DEFAULT_CACHE_TIMEOUT)
    elif len(bits) == 4:
        if bits[2] == 'as':
            return RandomClassifiedsNode(bits[1], bits[3], DEFAULT_CACHE_TIMEOUT)
        elif bits[2] == 'for':
            return RandomClassifiedsNode(bits[1], DEFAULT_VARNAME, bits[3])
        else:
            raise template.TemplateSyntaxError, "'%s' tag requires one, three, or five arguments.\n{% get_random_classifieds [number of ads] (as [varname]) (for [cache_timeout (in seconds)]) %}" % bits[0]
    elif len(bits) == 6:
        if bits[2] == 'as' and bits[4] == 'for':
            return RandomClassifiedsNode(bits[1], bits[3], bits[5])
        else:
            raise template.TemplateSyntaxError, "'%s' tag requires one, three, or five arguments.\n{% get_random_classifieds [number of ads] (as [varname]) (for [cache_timeout (in seconds)]) %}" % bits[0]
    else:
        raise template.TemplateSyntaxError, "'%s' tag requires one, three, or five arguments.\n{% get_random_classifieds [number of ads] (as [varname]) (for [cache_timeout (in seconds)]) %}" % bits[0]

class ClassifiedColsNode(CachedContextUpdatingNode):
    def __init__(self, number_cols, varname, sub_category_id):
        self.num_cols = int(number_cols)
        self.varname = varname
        if sub_category_id:
            self.sub_category_id = sub_category_id
        else:
            self.sub_category_id = 'all'
        self.cache_timeout = 0
    
    def __unicode__(self):
        return "<ClassifiedColsNode>"
    
    def get_cache_key(self, context):
        return "populous.advertising.classifieds.templatetags.columns:%s:%s:%s:%s" % (self.sub_category_id, self.varname, self.num_cols, settings.SITE_ID)
    
    def get_content(self, context):
        if self.sub_category_id != 'all':
            try:
                category = ClassifiedSubCategory.objects.get(cat_id=self.sub_category_id)
                ad_list = category.classifiedad_set.all()
            except:
                return '<!-- Error: No classified category with the ID %s could be found -->' % self.sub_category_id
        else:
            ad_list = ClassifiedAd.objects.all()
        
        print ad_list
        
        if len(ad_list) == 0:
            context[self.varname] = ad_dict
            raise template.TemplateSyntaxError, '%s' % ad_dict
            return '<!-- Empty List: There are no classifieds in this category -->'
        
        column_length = len(ad_list) / self.num_cols
        cursor = 0
        i = 0
        col_dict = {}
        
        print '\n\nstarting loop'
        
        while i < self.num_cols:
            if len(ad_list) - cursor <= column_length:
                col_dict['col%s' % (i+1)] = ad_list[cursor:]
            else:
                col_dict['col%s' % (i+1)] = ad_list[cursor:cursor+column_length]
            cursor += column_length
            i += 1
        context[self.varname] = col_dict
        return ''

def GetClassifiedCols(parser, token):
    """
    Gets [number of columns] columns of classified ads from the optional [from sub_category_id] and returns them as the context item [varname].
    If no [section_id] is provided, it will be assumed that all sub-categories are requested and return all classified ads in [number of columns] columns.
    
    Syntax::
    
        {% get_classified_cols [number of columns] [as varname] [from sub_category_id] %}
    """
    bits = token.contents.split()
    if not int(bits[1]) > 0:
        raise template.TemplateSyntaxError, "'%s' requires the first argument to be a positive integer" % bits[0]
    if len(bits) == 4:
        if bits[2] == 'as':
            return ClassifiedColsNode(bits[1], bits[3], None)
        else:
            raise template.TemplateSyntaxError, "'%s' tag requires the second argument to be 'as'." % bits[0]
    elif len(bits) == 6:
        if bits[2] == 'as' and bits[4] == 'from':
            return ClassifiedColsNode(bits[1], bits[3], bits[5])
        else:
            raise template.TemplateSyntaxError, "'%s' tag requires the second argument to be 'as' and the fourth argument to be 'from'." % bits[0]
    else:
        raise template.TemplateSyntaxError, "'%s' tag requires three or five arguments." % bits[0]

register.tag('get_classified_cols', GetClassifiedCols)
register.tag('get_placement_frame', DoGetPlacementFrame)
register.tag('get_random_classifieds', GetRandomClassifieds)
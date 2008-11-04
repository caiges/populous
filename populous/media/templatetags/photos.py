from django import template
from populous.media.models import Photo
from populous.core.parts.templatetags import CachedNode
from django.conf import settings
import datetime, re

def thumbnail(value, arg):
    "Input is the URL of an image; output is the URL of that image as a thumbnail with specified width"
    bits = value.split('/')
    bits[-1] = re.sub(r'(?i)\.(gif|jpg|png|jpeg)$', '_t%s.\\1' % arg, bits[-1])
    return '/'.join(bits)
    

class LatestPhotoNode(CachedNode):
    def __init__(self, varname):
        self.varname = varname
        self.cache_timeout = 180
        
    def get_cache_key(self, context):
        return "populous.media.templatetags.photos.do_get_latest:%s" % (settings.SITE_ID)

    def get_content(self, context):
        context[self.varname] = photos.get_object(order_by=('-creation_date',), creation_date__lte=datetime.datetime.now(), sites__id__exact=settings.SITE_ID, limit=1)
        return ""

def do_latest_photo(parser, token):
    """
    Gets the most recent photo whose creation date is not in the future for the current site.  If a variable name is
    specified, the photo will be added to the current context with that variable name, otherwise the photo will be
    called ``latest_photo``.

    Syntax::  
    
        {% get_latest_photo [as varname] %}        
    """
    bits = token.contents.split() 
    if len(bits) == 1:
        varname = 'latest_photo'
    elif len(bits) == 3:
        varname = bits[2]
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes either zero or two arguments" % bits[0]
    return LatestPhotoNode(varname)    

class LatestPhotoListNode(CachedNode):
    def __init__(self, varname, limit):
        self.varname = varname
        self.limit = limit

    def get_cache_key(self, context):
        return "populous.media.templatetags.photos.do_get_latest_photo_list:%s" % (settings.SITE_ID)

    def get_content(self, context):
        context[self.varname] = photos.get_list(order_by=('-creation_date',), creation_date__lte=datetime.datetime.now(), limit=self.limit)
        return "" 

def do_latest_photos_list(parser, token):
    """
    Gets a list of the most recent photos whose creation date is not in the future for the current site.  If a variable name is
    specified, the photos will be added to the current context with that variable name, otherwise the photo will be
    called ``latest_photos_list``.

    Syntax::                                            

        {% get_latest_photos_list [limit] [as varname] %}        
    """
    bits = token.contents.split() 
    if len(bits) == 1:
        varname = 'latest_photos_list'
    elif len(bits) == 2:
        varname = 'latest_photos_list'
        limit = bits[1]
    elif len(bits) == 4:
        varname = bits[3]
        limit = bits[1]
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes zero one or three arguments" % bits[0]
    return LatestPhotoListNode(varname, limit)

class PhotoByIDNode(CachedNode):
    def __init__(self, photo_id, varname):
        self.photo_id = photo_id
        self.varname = varname

    def get_cache_key(self, context):
        return "populous.media.templatetags.photos.do_get_latest_photo_list:%s" % (settings.SITE_ID)

    def get_content(self, context):
        if photos.get_object(pk=self.photo_id):
            context[self.varname] = photos.get_object(pk=self.photo_id)
            return "" 
        else:
            return "<!-- An error occured trying to return the photo you requested -->"

def get_photo_by_id(parser, token):
    """
    Gets a single photo by it's ID and pass it back as a context element accessable through the varname.

    Syntax::                                            

        {% get_photo_by_id [ID] [as varname] %}        
    """
    bits = token.contents.split() 
    if len(bits) == 3:
        photo_id = bits[1]
        varname = bits[2]
        return PhotoByIDNode(photo_id, varname)
    else:
        raise template.TemplateSyntaxError, "'%s' tag takes 2 arguments" % bits[0]
        return ''
                       
register = template.Library()
register.filter('thumbnail', thumbnail) 
register.tag('get_latest_photo', do_latest_photo)
register.tag('get_latest_photos_list', do_latest_photos_list)
register.tag('get_photo_by_id', get_photo_by_id)
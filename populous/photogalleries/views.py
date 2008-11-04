from django.core import paginator
from django.http import Http404, HttpResponse
from django.template import RequestContext as Context, loader

from populous.core.parts.xheaders import populate_xheaders
from populous.photogalleries.models import Gallery, GallerySet

def gallery_detail(request, gallery_slug, is_xml=False, is_flash=False):
    """
    Gallery detail page

    Templates: `media/gallery_detail`
    Context:
        gallery:
            `media.galleries` object
        photo_list:
            list of `media.galleryphotos` in the gallery
    """
    try:
        gal = Gallery.on_site.get(slug__exact=gallery_slug)
    except Gallery.DoesNotExist:
        raise Http404
    if is_xml:
        t = loader.select_template(["media/gallery_xml_%s_detail.html" % gal.template_prefix, "media/gallery_xml_detail.html"])
    elif is_flash:
        t = loader.select_template(["media/gallery_flash_%s_detail.html" % gal.template_prefix, "media/gallery_flash_detail.html"])
    else:
        t = loader.select_template(["media/gallery_%s_detail.html" % gal.template_prefix, "media/gallery_detail.html"])
    c = Context(request, {
        'gallery': gal,
        'photo_list': gal.galleryphoto_set.all(),
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, 'media', Gallery, gal.id)
    return response

def gallery_set_detail(request, slug, is_xml=None, is_flash=None):
    try:
        set = GallerySet.on_site.get(slug=slug)
    except GallerySet.DoesNotExist:
        raise Http404
    pag = paginator.ObjectPaginator(set.gallery_set.all(), 20)
    try:
        page_number = int(request.GET.get('page', 1)) - 1
    except ValueError:
        page_number = 0
    try:
        gallery_list = pag.get_page(page_number)
    except paginator.InvalidPage:
        raise Http404
    if is_xml:
        t = loader.select_template(["%s_xml" % set.template_name, 'media/galleryset_xml_detail.html'])
    elif is_flash:
        t = loader.select_template(["%s_flash" % set.template_name, 'media/galleryset_flash_detail.html'])
    else:
        t = loader.select_template([set.template_name, 'media/galleryset_detail.html'])
    c = Context(request, {
        'object': set,
        'gallery_list': gallery_list,
        'has_next_page': pag.has_next_page(page_number),
        'has_previous_page': pag.has_previous_page(page_number),
        'pages': pag.pages,
        'next_page': page_number + 2,
        'previous_page': page_number,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, 'media', GallerySet, set.id)
    return response
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.paginator import Paginator
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import date_based, list_detail
from populous.blogs.models import Blog, BlogCollection

NUM_BLOGS_LIMIT = 10
NUM_BLOGCOLLECTIONS_LIMIT = 5

def blogs_index(request):
    blog_list = Blog.objects.recently_updated()[:NUM_BLOGS_LIMIT]
    blog_collection_list = BlogCollection.objects.all()[:NUM_BLOGCOLLECTIONS_LIMIT]
    
    t = loader.get_template('blogs/index.html')
    c = RequestContext(request, {
        'blogs': blog_list,
        'blog_collections': blog_collection_list,
    })
    return HttpResponse(t.render(c))

def blogs_list(request):
    t = loader.get_template('blogs/blog_index.html')
    c = RequestContext(request, {
        'blogs': Blogs.ojbects.recently_updated(),
    })
    return HttpResponse(t.render(c))

def collection_index(request):
    t = loader.get_template('blogs/collection_index.html')
    c = RequestContext(request, {
        'collections': BlogCollection.objects.all(),
    })
    return HttpResponse(t.render(c))

def collection_detail(request, slug):
    blog_collection = get_object_or_404(BlogCollection, slug=slug)
    return list_detail.object_detail(request,
        queryset = BlogCollection.objects.all(),
        slug_field = 'slug',
        slug = slug,
        template_name = blog_collection.template_name or 'blogs/collection_default.html')

def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_index(request, 
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        extra_context = {'blog': blog},
        template_name = blog.template_name_blog or 'blogs/entry_archive_index.html')

def blog_archive_year(request, blog_slug, year):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_year(request,
        year = year,
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        extra_context = {'blog': blog},
        template_name = blog.template_name_date_archive or 'blogs/entry_archive_year.html')

def blog_archive_month(request, blog_slug, year, month):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_month(request,
        year=year,
        month=month,
        queryset=blog.entry_set.all(),
        date_field='pub_date',
        extra_context = {'blog': blog},
        template_name = blog.template_name_date_archive or 'blogs/entry_archive_month.html')

def blog_archive_day(request, blog_slug, year, month, day):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_day(request,
        year = year,
        month = month,
        day = day,
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        extra_context = {'blog': blog},
        template_name = blog.template_name_date_archive or 'blogs/entry_archive_day.html')

def blog_entry_detail(request, blog_slug, year, month, day, slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.object_detail(request,
        year = year,
        month = month,
        day = day,
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        slug_field = 'slug',
        slug = slug,
        extra_context = {'blog': blog},
        template_name = blog.template_name_entry or 'blogs/entry_detail.html')
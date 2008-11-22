from django.conf import settings
from django.contrib.sites.models import Site
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import date_based, list_detail
from populous.blogs.models import Blog, BlogCollection

def index(request):
    pass

def collection(request, slug):
    blog_collection = get_object_or_404(BlogCollection, slug=slug)
    return list_detail.object_detail(request,
        queryset = BlogCollection.objects.all(),
        slug_field = 'slug',
        slug = slug,
        template_name = blog_collection.template_name or 'blogs/collection_default.html')

def index(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_index(request, 
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        extra_context = {'blog': blog},
        template_name = blog.template_name_blog or 'blogs/entry_archive_index.html')

def archive_year(request, blog_slug, year):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_year(request,
        year = year,
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        extra_context = {'blog': blog},
        template_name = self.template_name_date_archive or 'blogs/entry_archive_year.html')

def archive_month(request, blog_slug, year, month):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_month(request,
        year=year,
        month=month,
        queryset=blog.entry_set.all(),
        date_field='pub_date',
        extra_context = {'blog': blog},
        template_name = self.template_name_date_archive or 'blogs/entry_archive_month.html')

def archive_day(request, blog_slug, year, month, day):
    blog = get_object_or_404(Blog, slug=blog_slug)
    return date_based.archive_day(request,
        year = year,
        month = month,
        day = day,
        queryset = blog.entry_set.all(),
        date_field = 'pub_date',
        extra_context = {'blog': blog},
        template_name = self.template_name_date_archive or 'blogs/entry_archive_day.html')

def entry_detail(request, blog_slug, year, month, day, slug):
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
        template_name = self.template_name_entry or 'blogs/entry_detail.html')
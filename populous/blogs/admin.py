from django.conf import settings
from django.contrib import admin

from populous.blogs.models import Blog, Entry

class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'tags', 'description', 'image', 'post_entry_note', 'contributors')
        }),
        ('Meta Data', {
            'fields': ('status', 'categories', 'default_comment_status', 'sites', 'template_name', 'slug')
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status', 'creation_date', 'update_date')
    list_filter = ('status',)
    search_field = ('title', 'description', 'post_entry_note', 'tags')
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'filebrowser/js/AddFileBrowser.js']

class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
            { 'fields': ('blog', 'title', 'tags', 'tease', 'entry', 'bylines', 'bylines_override', 'pub_date')}
        ),
        ('Meta Data',
            { 'fields': ('status', 'featured', 'comment_status', 'slug')}
        ),
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'blog', 'pub_date', 'status', 'comment_status')
    list_filter = ('status', 'featured', 'comment_status')
    search_fields = ('title', 'tease', 'entry', 'tags')
    date_hierarchy = "pub_date"

admin.site.register(Blog, BlogAdmin)
admin.site.register(Entry, EntryAdmin)
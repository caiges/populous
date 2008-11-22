from django.conf import settings
from django.contrib import admin

from populous.news.models import AdditionalContent, BreakingNews, Collection, CollectionBehavior, CollectionItem, Story, Dateline

class BreakingNewsInline(admin.StackedInline):
    model = BreakingNews

class CollectionBehaviorInline(admin.StackedInline):
    model = CollectionBehavior

class CollectionItemInline(admin.StackedInline):
    model = CollectionItem

class CollectionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'category', 'content', 'limit', 'start_date', 'end_date', 'template_name', 'sites')
        }),
    )
    list_display = ('title', 'url',)
    list_display_links = ('title', 'url',)
    search_fields = ('title', 'url', 'content',)
    inlines = (CollectionBehaviorInline, CollectionItemInline, BreakingNewsInline,)

class AdditionalContentInline(admin.StackedInline):
    model = AdditionalContent

class StoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('headline', 'subhead', 'tease', 'story', 'post_story_blurb', 'topics', 'categories')
        }),
        ('Meta data', {
            'fields': ('is_approved', 'pub_date', 'bylines', 'bylines_override', 'dateline', 'slug', 'comment_status', 'sites')
        }),
        ('Story Media', {
            'fields': ('lead_photo', 'lead_photo_has_headline', 'tease_photo')
        }),
    )
    date_hierarchy = "pub_date"
    list_display = ('headline', 'pub_date', 'update_date', 'is_approved')
    list_display_links = ('headline', )
    list_filter = ('is_approved', 'sites', 'comment_status')
    prepopulated_fields = {"slug": ("headline",)}
    search_fields = ['headline', 'subhead', 'tease', 'story', 'post_story_blurb']
    filter_horizontal = ('sites', 'categories', 'topics')
    inlines = (AdditionalContentInline,)
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'filebrowser/js/AddFileBrowser.js']

admin.site.register(Collection, CollectionAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Dateline)
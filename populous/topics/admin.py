from django.conf import settings
from django.contrib import admin
from topics.models import Topic, TopicCollection

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'category')
    search_fields = ('name', 'category')
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'filebrowser/js/AddFileBrowser.js']

admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicCollection)

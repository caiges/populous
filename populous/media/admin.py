from django.contrib import admin
from populous.media.models import AlternateVideo, Audio, BaseFileType, File, Photo, Video

class AudioAdmin(admin.ModelAdmin):
    list_display = ('title', 'type')
    list_filter = ('type', 'sites', 'categories')
    search_fields = ('title', 'file')

    class Media:
        js = ['/admin_media/filebrowser/js/AddFileBrowser.js']

class BaseFileTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type')
    list_filter = ('content_type',)

class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file')
    list_filter = ('type', 'sites')
    search_fields = ('title', 'file')

class PhotoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('file', 'caption', 'sites')}),
        ('Credit', {'fields': ('one_off_photographer', 'credit', 'date_created')}),
    )
    list_display = ('file', 'caption', 'date_created')
    list_filter = ('sites', 'date_created', 'categories')
    date_hierarchy = 'date_created'
    search_fields = ('caption', 'file')
    #js = ('/m/js/admin/photo_captions.js',)

class AlerternateVideoInlineAdmin(admin.TabularInline):
    model = AlternateVideo
    extra = 2

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'file')
    list_filter = ('sites', 'date_created', 'categories')
    date_hierarchy = 'date_created'
    search_fields = ('caption', 'url')
    inlines = (AlerternateVideoInlineAdmin,)
    filter_horizontal = ('categories',)

admin.site.register(Audio, AudioAdmin)
admin.site.register(BaseFileType, BaseFileTypeAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Video, VideoAdmin)
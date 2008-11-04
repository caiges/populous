from django.contrib import admin

from populous.photogalleries.models import Gallery, GalleryPhoto, GallerySet

class GallerySetAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'template_name', 'sites')}),
    )
    list_display = ('name',)
    list_filter = ('date_created', 'sites',)
    date_hierarchy = 'date_created'
    search_fields = ('name',)
    prepopulate_fields = {'slug': ('name',)}

class GalleryPhotoInlineAdmin(admin.TabularInline):
    model = GalleryPhoto
    extra = 10
    raw_id_fields = ('photo',)

class GalleryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'template_prefix', 'sites', 'audio')}),
    )
    list_display = ('name',)
    list_filter = ('date_created', 'sites')
    date_hierarchy = 'date_created'
    search_fields = ('name',)
    prepopulate_fields = {'slug': ('name',)}
    raw_id_fields = ('audio',)
    inlines = (GalleryPhotoInlineAdmin,)

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GallerySet, GallerySetAdmin)
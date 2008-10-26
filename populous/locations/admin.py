from django.contrib import admin
from models import Location, LocationType

class LocationTypeAdmin(admin.ModelAdmin):
    prepopulate_fields = {'slug': ('name_plural',)}
    list_display = ('name',)

class LocationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': (('name', 'slug',), 'display_name', 'abbreviation', 'use_abbreviation')
        }),
        ('Relational Information', {
            'fields': ('location_type', 'parent', 'default_for_type',)
        }),
        ('Address Information', {
            'classes': 'collapse',
            'fields': ('address1', 'address2', 'postal_code',)
        }),
        ('Extended Information', {
            'fields': ('short_description', 'description',)
        }),
        ('Geographical Information', {
            'fields': ('latitude', 'longitude', 'timezone',)
        }),
    )
    raw_id_fields = ('parent',)
    prepopulate_fields = {'slug': ('display_name', 'name')}
    list_filter = ('location_type', 'default_for_type')
    list_display = ('name', 'location_type', 'parent')
    search_fields = ('name', 'abbreviation',)

admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(Location, LocationAdmin)
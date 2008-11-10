from django.contrib import admin
from django.contrib.contenttypes import generic
from populous.places.models import School, Restaurant, Cuisine, PlaceOption, InlinePlaceOption

class SchoolAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("name",)}
    list_display = ('name', 'abbreviation', 'mascot_plural')
    raw_id_fields = ('location',)

class InlinePlaceOptionInline(generic.GenericTabularInline):
    model = InlinePlaceOption
    extra = 3

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [InlinePlaceOptionInline]
    #fieldsets = (
    #    ('Restaurant info',
    #        {'classes': 'wide', 'fields': ('location', 'icon', 'featured_date', 'cuisines', 'local', 'outdoor_seating', 'accept_reservations', 'accept_callaheads', 'kids_menu', 'party_room', 'live_music', 'has_delivery', 'has_buffet', 'ed_pick', 'num_vegetarian', 'num_vegan', 'num_tvs', 'disable_comments')}),
    #    ('Pricing',
    #        {'fields': ('price_low', 'price_high')}),
    #    ('Accepted payment methods',
    #        {'classes': 'wide', 'fields': ('pay_visa', 'pay_mastercard', 'pay_discover', 'pay_amex', 'pay_checks',)}),
    #)
    raw_id_fields = ('location',)

class CuisineAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name','slug',)}),
    )
    list_display = ('name', )
    search_fields = ('name',)
    
admin.site.register(School, SchoolAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(PlaceOption)
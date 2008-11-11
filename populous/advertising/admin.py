from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from populous.advertising.models import TextAd, GraphicAd, VideoAd, CouponCategory, \
                                        Coupon, ClassifiedSubCategory, ClassifiedCategory, \
                                        ClassifiedAd, UploadClassifiedAdSet, CurrentClassifiedAdSet, \
                                        Client, Placement, Statistic, ScheduledAd

DEFAULT_ADMIN_JS = ['js/jquery.js', 'js/related_content.js', 'js/generic.js',]
DEFAULT_ADMIN_FIELDS = [
        (None, {
            'fields': (('name', 'slug'), 'client',)
        }),
    ]

def fields(fields):
    """
    Helper function to extend default admin fields.
    
    Usage::
    
    class ExampleAdmin(admin.ModelAdmin):
        fields = fields(
            (_('Label'), {
                'fields': ('some', 'field', 'names',)
            })
        )
    """
    import copy
    return_fields = copy.copy(DEFAULT_ADMIN_FIELDS)
    return_fields.append(fields)
    return return_fields

class TextAdAdmin(admin.ModelAdmin):
    fields = fields(
        (_('Ad information'), {
            'fields': ('kicker', 'caption', 'decked_head', 'content', ('image_only', 'image'), ('link_only', 'link',),)
        })
    )
    js = (DEFAULT_ADMIN_JS, )
    prepopulate_fields = {'slug': ('name',)}
    list_display = ('name', 'client')
    search_fields = ('name', 'kicker', 'decked_head', 'content',)
    list_filter = ('image_only', 'link_only')
    list_select_related = True
    raw_id_fields = ('client',)

class GraphicAdAdmin(admin.ModelAdmin):
    fields = fields(
        (_('Ad information'), {
            'fields': ('image', 'url', )
        })
    )
    js = (DEFAULT_ADMIN_JS, )
    prepopulate_fields = {'slug': ('name',)}
    list_display = ('name', 'client',)
    search_fields = ('name', 'client__name', 'image', 'url',)
    list_select_related = True
    raw_id_fields = ('client',)
    save_as = True

class VideoAdAdmin(admin.ModelAdmin):
    fields = fields(
        (_('Ad information'), {
            'fields': ('video', 'url',)
        })
    )
    js = (DEFAULT_ADMIN_JS, )
    prepopulate_fields = {'slug': ('name',)}
    raw_id_fields = ('client',)

class CouponCategoryAdmin(admin.ModelAdmin):
    prepopulate_fields = {'slug': ('name',)}

class CouponAdmin(admin.ModelAdmin):
    fields = fields(
        (_('Ad information'), {
            'fields': ('headline', 'category', 'image', 'image_orientation',)
        })
    )
    js = (DEFAULT_ADMIN_JS, )
    prepopulate_fields = {'slug': ('name',)}
    raw_id_fields = ('client',)

class ClassifiedSubCategoryAdmin(admin.ModelAdmin):
    prepopulate_fields = {'slug': ('sub_category_id', 'name',)}

class ClassifiedCategoryAdmin(admin.ModelAdmin):
    prepopulate_fields = {'slug': ('name',)}

class ClassifiedAdAdmin(admin.ModelAdmin):
    prepopulate_fields = {'slug': ('name',)}
    
    
#####################
##  Admin Options  ##
#####################

class ClientAdmin(admin.ModelAdmin):
    fields = (
        (None, {
            'classes': 'wide',
            'fields': ('name', ('phone1', 'phone2',), 'fax', 'email', 'website',)
        }),
        (_('Contact information'), {
            'classes': 'wide',
            'fields': ('address1', 'address2', 'city', 'state', 'zipcode', 'country', )
        }),
    )
    js = ('js/jquery.js', 'js/related_content.js', )
    list_display = ('name', 'get_client_ad_count')
    search_fields = ('name', 'phone1', 'phone2', 'fax', 'email', 'website', 'address1', 'address2', 'city', 'state', 'ziode', 'country',)
    list_select_related = True

class PlacementStackedInline(admin.StackedInline):
    model = ScheduledAd
    extra = 1

class PlacementAdmin(admin.ModelAdmin):
    fields = (
        (None, {
            'fields': (('location', 'type_placement'), 'notes', 'sites', 'allowable_ad_types', 'image', 'height', 'width', 'template', 'num_ads', 'orientation')
        }),
        (_('Random properties'), {
            'fields': ('random', 'random_ad_types',),
            'classes': 'collapse',
        }),
    )
    js = ('js/advertising/jquery.js', 'js/advertising/thickbox.js', 'js/advertising/generic.js', 'js/advertising/ad_behavior.js', 'js/advertising/placements.js',)
    list_display = ('location', 'notes', 'type_placement', 'get_ad_count')
    list_filter = ('type_placement',)
    list_select_related = True
    filter_horizontal = ('random_ad_types', )
    ordering = ('location',)
    inlines = (PlacementStackedInline,)

class StatisticAdmin(admin.ModelAdmin):
    fields = (
        (None, {
            'fields': (('ad_type', 'ad_id'), 'placement', ('clickthrough_count', 'impression_count'), ('start_date', 'end_date'),)
        }),
    )
    js = ('js/jquery.js', 'js/generic.js')
    list_display = ('get_advertisement', 'placement', 'clickthrough_count', 'impression_count',  'ad_type',)
    list_select_related = True
    date_hierarchy = 'start_date'

admin.site.register(Client, ClientAdmin)
admin.site.register(Placement, PlacementAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(ScheduledAd)

admin.site.register(TextAd, TextAdAdmin)
admin.site.register(GraphicAd, GraphicAdAdmin)
admin.site.register(VideoAd, VideoAdAdmin)
admin.site.register(CouponCategory, CouponCategoryAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(ClassifiedSubCategory, ClassifiedSubCategoryAdmin)
admin.site.register(ClassifiedCategory, ClassifiedCategoryAdmin)
admin.site.register(ClassifiedAd, ClassifiedAdAdmin)
admin.site.register(UploadClassifiedAdSet)
admin.site.register(CurrentClassifiedAdSet)
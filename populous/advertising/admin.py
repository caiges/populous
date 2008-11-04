from populous.advertising.models import TextAd, GraphicAd, VideoAd, CouponCategory,
                                        Coupon, ClassifiedSubCategory, ClassifiedCategory,
                                        ClassifiedAd, UploadClassifiedAdSet, CurrentClassifiedAdSet

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
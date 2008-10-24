from django.contrib import admin
from populous.categories.models import Category

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('parent', 'name')}),
    )
    list_display = ('representation',)
    search_fields = ('representation',)

admin.site.register(Category, CategoryAdmin)

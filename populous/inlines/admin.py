from django.contrib import admin
from populous.inlines.models import RegisteredInline, AllowedField

class AllowedFieldInline(admin.StackedInline):
    filter_horizontal = ('sites',)
    model = AllowedField
    extra = 3

class RegisteredInlineAdmin(admin.ModelAdmin):
    inlines = (AllowedFieldInline,)
    
    def has_add_permission(self, request):
        """
        Inlines are not meant to be added through the admin interface.
        """
        return False

admin.site.register(RegisteredInline, RegisteredInlineAdmin)
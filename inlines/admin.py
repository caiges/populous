from django.contrib import admin
from populous.inlines.models import RegisteredInline, AllowedField

class AllowedFieldInline(admin.TabularInline):
    model = AllowedField
    extra = 3

class RegisteredInlineAdmin(admin.ModelAdmin):
    inlines = (AllowedFieldInline,)

admin.site.register(RegisteredInline, RegisteredInlineAdmin)
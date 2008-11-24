from django.conf import settings
from django.contrib import admin

from populous.blogs.models import Blog, BlogCollection, Entry

# General Note Regarding Permissions
# 
# Because of the long-term need for a multi-user bloggin system, specialized permissions
#   must be implemented.  In order to achieve our implementation of blog-per-user, each
#   new user must initially be given the permissions to add/change/remove both blogs and
#   entries.  This will be left to the registration application.
# Superusers must retain full control.
# A BlogCollection has moderators, which have full control of the collection, and all
#   subsequent blogs and their entries.
# A Blog has a creator, moderators, and contributors.  A creator has full control of the
#   blog and its entries.  Moderators are the same as the creator but without the ability
#   to delete the blog.  Contributors can only add new entries and change new entries to
#   the blog.
#
# TODO:
#   - Permissions for BlogCollection moderators
#   - Restrict add permission of entries to blogs

class BlogAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'tags', 'description', 'image', 'post_entry_note', 'moderators', 'contributors')
        }),
        ('Meta Data', {
            'fields': ('status', 'categories', 'default_comment_status', 'sites', 'slug')
        }),
        ('Template Overrides', {
            'fields': ('template_name_blog', 'template_name_date_archive', 'template_name_entry')
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status', 'creation_date', 'update_date')
    list_filter = ('status',)
    search_field = ('title', 'description', 'post_entry_note', 'tags')
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'filebrowser/js/AddFileBrowser.js']
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if not obj.pk:
            obj.creator = request.user
        obj.save()
    
    def queryset(self, request):
        qs = self.model._default_manager.get_query_set()
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        lst = [ elem for elem in qs if self.has_change_permission(request, elem) or self.has_change_permission(request, elem) ]
        # print lst  # TODO: Implement this as a queryset
        return qs
    
    def has_add_permission(self, request):
        # Check for standard permissions
        opts = self.opts
        has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_add_permission())
        
        # If the user has created a blog and is not a superuser, return False
        # This ensures that any user can have a personal blog, but preserves superuser permissions.
        if has_perm and Blog.objects.filter(creator = request.user) and not request.user.is_superuser:
            has_perm = False
        return has_perm
    
    def has_change_permission(self, request, obj=None):
        # Check for standard permissions
        opts = self.opts
        has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())
        
        if obj and has_perm and not (request.user.is_superuser or obj.creator == request.user or request.user in obj.moderators.all()):
            has_perm = False
        return has_perm
    
    def has_delete_permission(self, request, obj=None):
        # Check for standard permissions
        opts = self.opts
        has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission())
        
        if obj and has_perm and not (obj.creator == request.user or request.user.is_superuser):
            has_perm = False
        return has_perm

class BlogCollectionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'blogs', 'moderators', 'template_name')
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title',)
    search_field = ('title', 'description',)

class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None,
            { 'fields': ('blog', 'title', 'tags', 'tease', 'entry', 'bylines', 'bylines_override', 'pub_date')}
        ),
        ('Meta Data',
            { 'fields': ('status', 'featured', 'comment_status', 'slug')}
        ),
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'blog', 'pub_date', 'status', 'comment_status')
    list_filter = ('status', 'featured', 'comment_status')
    search_fields = ('title', 'tease', 'entry', 'tags')
    date_hierarchy = "pub_date"
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if not obj.pk:
            obj.creator = request.user
        obj.save()
    
    # No Need to override this yet
    # However restrictions must be imposed on what blog a user can actually create an entry for.
    #def has_add_permission(self, request):
    #    # Check for standard permissions
    #    opts = self.opts
    #    has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_add_permission())
    #    return has_perm
    
    def has_change_permission(self, request, obj=None):
        # Check for standard permissions
        opts = self.opts
        has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_change_permission())
        
        if obj and has_perm and not (request.user.is_superuser or obj.creator == request.user or request.user in obj.blog.moderators.all()):
            has_perm = False
        return has_perm
    
    def has_delete_permission(self, request, obj=None):
        # Check for standard permissions
        opts = self.opts
        has_perm = request.user.has_perm(opts.app_label + '.' + opts.get_delete_permission())
        
        if obj and has_perm and not (request.user.is_superuser or obj.creator == request.user or request.user in obj.blog.moderators.all()):
            has_perm = False
        return has_perm

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCollection, BlogCollectionAdmin)
admin.site.register(Entry, EntryAdmin)
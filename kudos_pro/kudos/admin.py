# from django.contrib import admin
# from .models import Organization

# # Register your models here.
# admin.site.register(Organization)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organization, User, Kudo

# Customize how the User model appears in admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'organization', 'remaining_kudos', 'last_kudo_reset', 'is_staff')
    list_filter = ('organization', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Organization', {'fields': ('organization', 'remaining_kudos', 'last_kudo_reset')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'organization'),
        }),
    )
    search_fields = ('username', 'email', 'organization__name')
    ordering = ('username',)

# Custom admin for Kudo model
class KudoAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at', 'truncated_message')
    list_filter = ('created_at', 'from_user__organization')
    search_fields = ('from_user__username', 'to_user__username', 'message')
    date_hierarchy = 'created_at'
    
    def truncated_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    truncated_message.short_description = 'Message'

# Register your models here
admin.site.register(Organization)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Kudo, KudoAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Organization, User, Kudo

class OrganizationAdminForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
        
    def clean_id(self):
        # Handle both UUID strings and UUID objects
        from django.core.validators import validate_uuid4
        from django.core.exceptions import ValidationError
        id_value = self.cleaned_data.get('id')
        if id_value:
            try:
                validate_uuid4(str(id_value))
            except ValidationError:
                raise forms.ValidationError("Enter a valid UUID.")
        return id_value

class CustomUserAdmin(UserAdmin):
    form = OrganizationAdminForm  # Use the same form for User model
    list_display = ('username', 'email', 'organization', 'remaining_kudos', 'is_staff')
    list_filter = ('organization', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Organization Info', {'fields': ('organization', 'remaining_kudos', 'last_kudo_reset')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Organization Info', {'fields': ('organization', 'remaining_kudos')}),
    )

class KudoAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created_at')
    list_filter = ('created_at', 'from_user__organization')
    readonly_fields = ('id', 'created_at')

# Register models
admin.site.register(Organization)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Kudo, KudoAdmin)
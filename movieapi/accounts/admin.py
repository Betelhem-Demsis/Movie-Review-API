from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    # Columns to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
    
    # Fields that can be searched in the user list
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Grouping fields into sections in the admin form
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

# Register the CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)

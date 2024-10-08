from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
    search_fields = ('username', 'email', 'first_name', 'last_name')
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

admin.site.register(CustomUser, CustomUserAdmin)

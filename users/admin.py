from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Customize the fields shown in the user list view
    list_display = ('username', 'email', 'custom_username', 'permission_level', 'is_staff')

    # Add filters for permission level and is_staff
    list_filter = ('permission_level', 'is_staff', 'is_superuser', 'is_active', 'groups')

    # Enable search by username, email, and custom username
    search_fields = ('username', 'email', 'custom_username')

    # Customize what fields are editable in the user form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'custom_username', 'profile_picture', 'profile_description')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'permission_level')}),
        ('Projects', {'fields': ('requested_projects', 'joined_projects')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add fields for creating new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'custom_username', 'permission_level')}
         ),
    )

    # Customize the ordering of the user list
    ordering = ('username',)


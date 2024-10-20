from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Customize what fields are shown in the list display
    list_display = ('username', 'email', 'custom_username', 'permission_level', 'is_staff')
    # Enable search by username and email
    search_fields = ('username', 'email', 'custom_username')
    # Customize what fields are editable in the user form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'custom_username', 'profile_picture', 'profile_description')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'permission_level')}),
        ('Projects', {'fields': ('requested_projects', 'joined_projects')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

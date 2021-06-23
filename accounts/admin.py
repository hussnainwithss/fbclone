from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Class regsitsers the CustomUser model in the django admin dashboard
    and defines the filters and how the customuser model views
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active','is_superuser')
    list_filter = ('email', 'is_staff', 'is_active','is_superuser')
    fieldsets = (
        ('Basic Info', {'fields': ('email', 'password','first_name','last_name',)}),
        ('Permissions', {'classes': ('collapse',),'fields': ('is_staff', 'is_active',
        'is_superuser','groups','user_permissions')}),
    )
    add_fieldsets = (
        ('Basic Info', {'fields': ('email', 'password1','password2','first_name',
        'last_name',)}),('Permissions', {'classes': ('collapse',),
        'fields': ('is_staff', 'is_active','is_superuser','groups','user_permissions')}),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)

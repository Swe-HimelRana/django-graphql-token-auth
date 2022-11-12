
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from account import models



# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    search_fields = ('email', 'first_name', 'last_name', 'phone',
                     'joined_date')
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_staff']
    list_filter = ('is_suspended', 'is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'is_phone_verified', 'is_identity_verified')
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password', 'first_name', 'last_name')}),
        (_('Personal Info'), {
         'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_suspended',
                    'is_email_verified',
                    'is_phone_verified',
                    'is_identity_verified',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'joined_date')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
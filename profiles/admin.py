from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client


class CustomUserAdmin(UserAdmin):

    list_display = ('full_name', 'email', 'is_staff', 'is_superuser', 'role')
    ordering = ('full_name',)
    search_fields = ('full_name', 'email')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_active', 'is_staff', 'role'),
        }),
    )

admin.site.register(User, CustomUserAdmin)


class ClientAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'email', 'company_name', 'user_contact', 'sales_contact', 'last_contact')
    ordering = ('full_name',)
    search_fields = ('full_name', 'email', 'company_name', 'user_contact__full_name', 'sales_contact__full_name')

admin.site.register(Client, ClientAdmin)

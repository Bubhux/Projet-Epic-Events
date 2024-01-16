from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db.models import Count, Subquery, OuterRef

from .models import User, Client


class CustomUserAdmin(UserAdmin):

    list_display = ('full_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'role')
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
            'fields': ('email', 'full_name', 'password1', 'password2', 'phone_number', 'is_active', 'is_staff', 'role', 'date_joined'),
        }),
    )


class ClientAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'email', 'company_name', 'sales_contact', 'last_contact')
    ordering = ('full_name',)
    search_fields = ('full_name', 'email', 'company_name', 'user_contact__full_name', 'sales_contact__full_name')


class GroupAdmin(admin.ModelAdmin):

    list_display = ('name', 'total_users')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            client_count=Subquery(Client.objects.filter(user_contact__groups=OuterRef('id')).values('user_contact__groups').annotate(count=Count('id')).values('count')[:1])
        )
        return queryset

    def total_users(self, obj):
        if obj.name == 'Client':
            return obj.client_count
        elif obj.name == 'Staff':
            staff_group = Group.objects.get(name='Staff')
            return staff_group.user_set.count()

    total_users.short_description = "Nombre d'utilisateurs"


admin.site.register(User, CustomUserAdmin)
admin.site.register(Client, ClientAdmin)

# Enregistre le nouveau admin.ModelAdmin pour Group
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
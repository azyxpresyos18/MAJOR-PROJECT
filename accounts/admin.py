from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    model = Employee
    list_display  = ['email', 'full_name', 'role', 'department', 'is_active', 'date_joined']
    list_filter   = ['role', 'department', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering      = ['last_name', 'first_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Role & Department', {'fields': ('role', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2',
                'first_name', 'last_name', 'role', 'department'
            ),
        }),
    )

    readonly_fields = ['date_joined', 'last_login']
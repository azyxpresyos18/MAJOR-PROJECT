from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'dept_type', 'client', 'is_active', 'created_at']
    list_filter   = ['dept_type', 'is_active', 'client']
    search_fields = ['name', 'client__name']
    ordering      = ['name']
    readonly_fields = ['created_at']
    autocomplete_fields = ['client']

    fieldsets = (
        (None, {'fields': ('name', 'dept_type', 'description', 'client', 'is_active')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
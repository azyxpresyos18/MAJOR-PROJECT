from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ['name', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['name']
    ordering      = ['name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('name', 'description', 'logo', 'is_active')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
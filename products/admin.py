from django.contrib import admin
from .models import Product, ProductCategory


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name']
    ordering      = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'client', 'department', 'category', 'status', 'created_at']
    list_filter   = ['status', 'client', 'department', 'category']
    search_fields = ['name', 'client__name', 'department__name']
    ordering      = ['client', 'name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['client', 'department', 'category']

    fieldsets = (
        (None, {'fields': ('name', 'description', 'image', 'status')}),
        ('Classification', {'fields': ('client', 'department', 'category')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    actions = ['mark_active', 'mark_inactive']

    @admin.action(description='Mark selected products as active')
    def mark_active(self, request, queryset):
        queryset.update(status=Product.ACTIVE)

    @admin.action(description='Mark selected products as inactive')
    def mark_inactive(self, request, queryset):
        queryset.update(status=Product.INACTIVE)
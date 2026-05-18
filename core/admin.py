from django.contrib import admin
from .models import Client, Department, Product, Location, Schedule


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'category']
    list_filter = ['client', 'category']
    search_fields = ['name', 'client__name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'is_available']
    list_filter = ['city', 'is_available']
    search_fields = ['name', 'city']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['client', 'product', 'location', 'scheduled_date', 'scheduled_time', 'status']
    list_filter = ['status', 'client', 'department']
    search_fields = ['client__name', 'product__name', 'location__name', 'assigned_to']
    list_editable = ['status']
    date_hierarchy = 'scheduled_date'

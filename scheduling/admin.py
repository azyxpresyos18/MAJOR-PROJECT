from django.contrib import admin
from .models import Schedule, Mall


@admin.register(Mall)
class MallAdmin(admin.ModelAdmin):
    list_display  = ['name', 'city', 'is_active']
    list_filter   = ['city', 'is_active']
    search_fields = ['name', 'address']
    ordering      = ['name']


class ScheduleProductInline(admin.TabularInline):
    model = Schedule.products.through
    extra = 1
    verbose_name = 'Product'
    verbose_name_plural = 'Products in this schedule'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display  = [
        'title', 'client', 'mall', 'department',
        'assigned_to', 'start_datetime', 'end_datetime', 'status'
    ]
    list_filter   = ['status', 'client', 'mall', 'department']
    search_fields = ['title', 'client__name', 'mall__name']
    ordering      = ['start_datetime']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['client', 'mall', 'department', 'assigned_to']
    inlines = [ScheduleProductInline]
    exclude = ['products']

    fieldsets = (
        (None, {'fields': ('title', 'status', 'notes')}),
        ('Assignment', {'fields': ('client', 'department', 'mall', 'assigned_to')}),
        ('Schedule', {'fields': ('start_datetime', 'end_datetime')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    actions = ['mark_confirmed', 'mark_cancelled']

    @admin.action(description='Mark selected schedules as confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Schedule.CONFIRMED)

    @admin.action(description='Mark selected schedules as cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Schedule.CANCELLED)
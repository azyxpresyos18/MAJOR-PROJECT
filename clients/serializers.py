from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    product_count    = serializers.SerializerMethodField()
    department_count = serializers.SerializerMethodField()
    schedule_count   = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            'id', 'name', 'description', 'logo',
            'is_active', 'created_at', 'updated_at',
            'product_count', 'department_count', 'schedule_count'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_product_count(self, obj):
        return obj.products.count()

    def get_department_count(self, obj):
        return obj.departments.count()

    def get_schedule_count(self, obj):
        return obj.schedules.count()


class ClientMinimalSerializer(serializers.ModelSerializer):
    """Lightweight serializer for use inside nested representations."""
    class Meta:
        model = Client
        fields = ['id', 'name', 'logo']
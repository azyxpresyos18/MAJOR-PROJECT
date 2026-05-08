from rest_framework import serializers
from .models import Department
from clients.serializers import ClientMinimalSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    client_detail    = ClientMinimalSerializer(source='client', read_only=True)
    employee_count   = serializers.SerializerMethodField()
    product_count    = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'dept_type', 'description',
            'client', 'client_detail',
            'is_active', 'created_at',
            'employee_count', 'product_count'
        ]
        read_only_fields = ['created_at']
        extra_kwargs = {
            'client': {'write_only': True}
        }

    def get_employee_count(self, obj):
        return obj.employees.filter(is_active=True).count()

    def get_product_count(self, obj):
        return obj.products.count()


class DepartmentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'dept_type']
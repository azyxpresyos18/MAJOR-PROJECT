from rest_framework import serializers
from .models import Product, ProductCategory
from clients.serializers import ClientMinimalSerializer
from departments.serializers import DepartmentMinimalSerializer


class ProductCategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description', 'product_count']

    def get_product_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    client_detail     = ClientMinimalSerializer(source='client', read_only=True)
    department_detail = DepartmentMinimalSerializer(source='department', read_only=True)
    category_name     = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'image', 'status',
            'category', 'category_name',
            'client', 'client_detail',
            'department', 'department_detail',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'client':     {'write_only': True},
            'department': {'write_only': True},
            'category':   {'write_only': True},
        }

    def validate(self, data):
        # Ensure assigned department belongs to the same client
        department = data.get('department')
        client = data.get('client')
        if department and client:
            if department.client and department.client != client:
                raise serializers.ValidationError(
                    'Department does not belong to the selected client.'
                )
        return data


class ProductMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'status']
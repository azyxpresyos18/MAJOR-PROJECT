from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Department
from .serializers import DepartmentSerializer
from accounts.permissions import IsAdminOrManager


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('client').all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'client__name']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManager()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        client_id = self.request.query_params.get('client')
        dept_type = self.request.query_params.get('dept_type')
        is_active = self.request.query_params.get('is_active')
        if client_id:
            qs = qs.filter(client_id=client_id)
        if dept_type:
            qs = qs.filter(dept_type=dept_type)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        return qs

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        from accounts.serializers import EmployeeSerializer
        dept = self.get_object()
        employees = dept.employees.filter(is_active=True)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        from products.serializers import ProductSerializer
        dept = self.get_object()
        products = dept.products.select_related('client', 'category').all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
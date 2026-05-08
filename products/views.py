from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Product, ProductCategory
from .serializers import ProductSerializer, ProductCategorySerializer
from accounts.permissions import IsAdminOrManager, IsAdminOrManagerOrSupervisor


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManager()]
        return [IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        'client', 'department', 'category'
    ).all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'client__name', 'department__name']
    ordering_fields = ['name', 'status', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManagerOrSupervisor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        client_id  = self.request.query_params.get('client')
        dept_id    = self.request.query_params.get('department')
        category   = self.request.query_params.get('category')
        status     = self.request.query_params.get('status')
        if client_id:
            qs = qs.filter(client_id=client_id)
        if dept_id:
            qs = qs.filter(department_id=dept_id)
        if category:
            qs = qs.filter(category_id=category)
        if status:
            qs = qs.filter(status=status)
        return qs

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAdminOrManagerOrSupervisor])
    def set_status(self, request, pk=None):
        product = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Product.STATUS_CHOICES):
            return Response(
                {'detail': 'Invalid status.'},
                status=400
            )
        product.status = new_status
        product.save(update_fields=['status'])
        return Response(ProductSerializer(product).data)
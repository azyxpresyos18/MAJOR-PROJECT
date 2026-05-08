from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Schedule, Mall
from .serializers import (
    ScheduleSerializer, ScheduleStatusUpdateSerializer, MallSerializer
)
from accounts.permissions import IsAdminOrManager, IsAdminOrManagerOrSupervisor


class MallViewSet(viewsets.ModelViewSet):
    queryset = Mall.objects.all()
    serializer_class = MallSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManager()]
        return [IsAuthenticated()]


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related(
        'client', 'department', 'mall', 'assigned_to'
    ).prefetch_related('products').all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'client__name', 'mall__name']
    ordering_fields = ['start_datetime', 'status', 'created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManagerOrSupervisor()]
        if self.action == 'update_status':
            return [IsAdminOrManagerOrSupervisor()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        client_id   = self.request.query_params.get('client')
        mall_id     = self.request.query_params.get('mall')
        dept_id     = self.request.query_params.get('department')
        status      = self.request.query_params.get('status')
        assigned_to = self.request.query_params.get('assigned_to')
        date_from   = self.request.query_params.get('date_from')
        date_to     = self.request.query_params.get('date_to')

        if client_id:
            qs = qs.filter(client_id=client_id)
        if mall_id:
            qs = qs.filter(mall_id=mall_id)
        if dept_id:
            qs = qs.filter(department_id=dept_id)
        if status:
            qs = qs.filter(status=status)
        if assigned_to:
            qs = qs.filter(assigned_to_id=assigned_to)
        if date_from:
            qs = qs.filter(start_datetime__date__gte=date_from)
        if date_to:
            qs = qs.filter(end_datetime__date__lte=date_to)
        return qs

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        now = timezone.now()
        schedules = self.get_queryset().filter(
            start_datetime__gte=now,
            status__in=[Schedule.PENDING, Schedule.CONFIRMED]
        ).order_by('start_datetime')[:10]
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        schedules = self.get_queryset().filter(
            start_datetime__date=today
        ).order_by('start_datetime')
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'],
            permission_classes=[IsAdminOrManagerOrSupervisor])
    def update_status(self, request, pk=None):
        schedule = self.get_object()
        serializer = ScheduleStatusUpdateSerializer(
            schedule, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ScheduleSerializer(schedule).data)
from rest_framework import serializers
from .models import Schedule, Mall
from clients.serializers import ClientMinimalSerializer
from departments.serializers import DepartmentMinimalSerializer
from products.serializers import ProductMinimalSerializer
from accounts.serializers import EmployeeSerializer


class MallSerializer(serializers.ModelSerializer):
    schedule_count = serializers.SerializerMethodField()

    class Meta:
        model = Mall
        fields = ['id', 'name', 'address', 'city', 'is_active', 'schedule_count']

    def get_schedule_count(self, obj):
        return obj.schedules.count()


class ScheduleSerializer(serializers.ModelSerializer):
    client_detail     = ClientMinimalSerializer(source='client', read_only=True)
    department_detail = DepartmentMinimalSerializer(source='department', read_only=True)
    products_detail   = ProductMinimalSerializer(source='products', many=True, read_only=True)
    assigned_to_detail = EmployeeSerializer(source='assigned_to', read_only=True)
    mall_name         = serializers.CharField(source='mall.name', read_only=True)
    duration_hours    = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'title', 'status', 'notes',
            'client', 'client_detail',
            'department', 'department_detail',
            'products', 'products_detail',
            'mall', 'mall_name',
            'assigned_to', 'assigned_to_detail',
            'start_datetime', 'end_datetime', 'duration_hours',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'client':      {'write_only': True},
            'department':  {'write_only': True},
            'mall':        {'write_only': True},
            'assigned_to': {'write_only': True},
            'products':    {'write_only': True},
        }

    def get_duration_hours(self, obj):
        if obj.start_datetime and obj.end_datetime:
            delta = obj.end_datetime - obj.start_datetime
            return round(delta.total_seconds() / 3600, 2)
        return None

    def validate(self, data):
        start = data.get('start_datetime')
        end   = data.get('end_datetime')
        if start and end and end <= start:
            raise serializers.ValidationError(
                {'end_datetime': 'End time must be after start time.'}
            )

        # Conflict check: same mall, overlapping time, not cancelled
        mall = data.get('mall')
        if mall and start and end:
            qs = Schedule.objects.filter(
                mall=mall,
                start_datetime__lt=end,
                end_datetime__gt=start,
            ).exclude(status=Schedule.CANCELLED)

            # On update, exclude the current instance
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError(
                    {'mall': 'Another schedule already exists at this mall during that time.'}
                )
        return data


class ScheduleStatusUpdateSerializer(serializers.ModelSerializer):
    """Lightweight serializer just for updating schedule status."""
    class Meta:
        model = Schedule
        fields = ['status', 'notes']
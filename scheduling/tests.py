from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status

from accounts.models import Employee
from clients.models import Client
from departments.models import Department
from scheduling.models import Schedule, Mall


class ScheduleConflictTestCase(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(name='Test Client')
        self.mall = Mall.objects.create(
            name='Test Mall', address='123 St', city='Cebu City'
        )
        self.dept = Department.objects.create(
            name='Test Dept', dept_type='sales', client=self.client_obj
        )
        self.now = timezone.now()

        self.existing = Schedule.objects.create(
            title='Existing Schedule',
            client=self.client_obj,
            mall=self.mall,
            department=self.dept,
            start_datetime=self.now + timedelta(hours=1),
            end_datetime=self.now + timedelta(hours=5),
            status=Schedule.CONFIRMED,
        )

    def test_overlapping_schedule_same_mall_is_rejected(self):
        from scheduling.serializers import ScheduleSerializer
        data = {
            'title': 'Overlap Schedule',
            'client': self.client_obj.pk,
            'mall': self.mall.pk,
            'department': self.dept.pk,
            'start_datetime': self.now + timedelta(hours=3),
            'end_datetime':   self.now + timedelta(hours=7),
            'status': Schedule.PENDING,
        }
        serializer = ScheduleSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('mall', serializer.errors)

    def test_non_overlapping_schedule_same_mall_is_accepted(self):
        from scheduling.serializers import ScheduleSerializer
        data = {
            'title': 'Non-Overlap Schedule',
            'client': self.client_obj.pk,
            'mall': self.mall.pk,
            'department': self.dept.pk,
            'start_datetime': self.now + timedelta(hours=6),
            'end_datetime':   self.now + timedelta(hours=9),
            'status': Schedule.PENDING,
        }
        serializer = ScheduleSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_cancelled_schedule_does_not_block_slot(self):
        from scheduling.serializers import ScheduleSerializer
        self.existing.status = Schedule.CANCELLED
        self.existing.save()
        data = {
            'title': 'After Cancel',
            'client': self.client_obj.pk,
            'mall': self.mall.pk,
            'department': self.dept.pk,
            'start_datetime': self.now + timedelta(hours=2),
            'end_datetime':   self.now + timedelta(hours=4),
            'status': Schedule.PENDING,
        }
        serializer = ScheduleSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_end_before_start_is_rejected(self):
        from scheduling.serializers import ScheduleSerializer
        data = {
            'title': 'Bad Times',
            'client': self.client_obj.pk,
            'mall': self.mall.pk,
            'start_datetime': self.now + timedelta(hours=5),
            'end_datetime':   self.now + timedelta(hours=2),
        }
        serializer = ScheduleSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('end_datetime', serializer.errors)


class PermissionTestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.admin = Employee.objects.create_user(
            email='admin@demopower.com', password='admin1234',
            first_name='Admin', last_name='User', role=Employee.ADMIN
        )
        self.staff = Employee.objects.create_user(
            email='staff@demopower.com', password='staff1234',
            first_name='Staff', last_name='User', role=Employee.STAFF
        )
        self.client_obj = Client.objects.create(name='Perm Test Client')

    def _get_token(self, email, password):
        response = self.api_client.post('/api/auth/login/', {
            'email': email, 'password': password
        }, format='json')
        return response.data.get('access')

    def test_staff_cannot_create_client(self):
        token = self._get_token('staff@demopower.com', 'staff1234')
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.api_client.post('/api/clients/', {
            'name': 'Unauthorized Client'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_client(self):
        token = self._get_token('admin@demopower.com', 'admin1234')
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.api_client.post('/api/clients/', {
            'name': 'Authorized Client'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_request_is_rejected(self):
        self.api_client.credentials()
        response = self.api_client.get('/api/clients/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_staff_can_list_clients(self):
        token = self._get_token('staff@demopower.com', 'staff1234')
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.api_client.get('/api/clients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductDepartmentValidationTest(TestCase):
    def setUp(self):
        self.client_a = Client.objects.create(name='Client A')
        self.client_b = Client.objects.create(name='Client B')
        self.dept_a = Department.objects.create(
            name='Dept A', dept_type='sales', client=self.client_a
        )

    def test_product_rejects_mismatched_client_department(self):
        from products.serializers import ProductSerializer
        data = {
            'name': 'Bad Product',
            'client': self.client_b.pk,
            'department': self.dept_a.pk,
            'status': 'pending',
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_product_accepts_matching_client_department(self):
        from products.serializers import ProductSerializer
        data = {
            'name': 'Good Product',
            'client': self.client_a.pk,
            'department': self.dept_a.pk,
            'status': 'pending',
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
from rest_framework.permissions import BasePermission
from .models import Employee


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Employee.ADMIN


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            Employee.ADMIN, Employee.MANAGER
        ]


class IsAdminOrManagerOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            Employee.ADMIN, Employee.MANAGER, Employee.SUPERVISOR
        ]


class IsSelfOrAdmin(BasePermission):
    """Allow users to view/edit their own profile; admins can access anyone."""
    def has_object_permission(self, request, view, obj):
        return request.user.role == Employee.ADMIN or obj == request.user
from rest_framework import permissions
from django.conf import settings

class isSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class isEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.roll == settings.EMPLEADO)
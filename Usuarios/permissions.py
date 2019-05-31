from rest_framework import permissions
from django.conf import settings

class isSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_staff))

class isAdminUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        print("Primer Nivel")
        return bool(request.user and request.user.roll == settings.ADMIN)

    def has_object_permission(self, request, view, obj):
        """
        Método que filtra los permisos de acuerdo al Administrador
        de la Empresa.
        :param request:
        :param view:
        :param obj:
        :return: True: Si tiene los permisos
                 False: Si no tiene los permisos
        """
        print("Segundo Nivel")
        return request.user == obj.custom_user

class isAdminUserOwnerArea(permissions.BasePermission):
    def has_permission(self, request, view):
        print("Primer Nivel")
        return bool(request.user and request.user.roll == settings.ADMIN)

    def has_object_permission(self, request, view, obj):
        """
        Método que filtra los permisos de acuerdo al Administrador
        de la Empresa.
        :param request:
        :param view:
        :param obj:
        :return: True: Si tiene los permisos
                 False: Si no tiene los permisos
        """
        print("Segundo Nivel")
        return request.user == obj.id_empresa.custom_user


class isEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.roll == settings.EMPLEADO)


class is_admin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.roll == settings.ADMIN



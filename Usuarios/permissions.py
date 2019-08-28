from rest_framework import permissions
from django.conf import settings
from Usuarios.models import CustomUser
from Empresas.models import Area

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



class isAdminUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        print("Primer Nivel")
        print(request.user and request.user.is_superuser)
        return bool(request.user and request.user.is_superuser)

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
        print(request.user and request.user.is_superuser)
        return bool(request.user and request.user.is_superuser)

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
    message = 'Not allowed.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.roll == settings.EMPLEADO)


class IsAdmin(permissions.BasePermission):
    message = 'Not allowed.'
    def has_permission(self, request, view):
        return request.user.roll == settings.ADMIN


class IsUser(permissions.BasePermission):
    message = 'Not Allowed'

    def has_permission(self, request, view):
        if request.user.roll == settings.NONE:
            if request.user.is_staff == False:
                if request.user.is_superuser == False:
                    return True
        return False


class isGuard(permissions.BasePermission):
    """By: DEVCRACK
    Determine if the current Logged User is a Guard
    """""
    def has_permission(self, request, view):
        return request.user.roll == settings.VIGILANTE


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.roll == settings.EMPLEADO

class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.roll == settings.ADMIN or request.user.is_staff))

class is_staff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff

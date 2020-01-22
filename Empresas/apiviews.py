from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from .serializers import *
from Usuarios.permissions import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import Q


"""
Crea o Lista  una empresa
"""
class EmpresaList(generics.ListCreateAPIView):
    """
    Clase EmpresaList, lista todas las Empresas.
    Clase que hereda de ListCreateAPIView, provee un método GET
    que Lista todas empresas.
    Nota: Solo usuarios com permiso Staff pueden consumirla.
    """
    permission_classes = (isSuperAdmin, )
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isSuperAdmin,)
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaViewSet(viewsets.ModelViewSet):
    permission_classes = (isSuperAdmin, )
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaUpdate(generics.UpdateAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Empresa.objects.all()
    lookup_field = 'pk'
    serializer_class = EmpresaSerializers


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    Filtro para precargar informacion de un usuario.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmpresaFindSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']

    def get_queryset(self):
        user = self.request.user
        if user.roll == settings.ADMIN:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            print("id Company = " + str(id_company))

        if user.roll == settings.EMPLEADO:
            employee_company = Empleado.objects.filter(id_usuario=user)[0]
            id_company = employee_company.id_empresa
            print("id Company = " + str(id_company))

        return Empresa.objects.exclude(Q(id=id_company.id))


class AdministradorList(generics.ListCreateAPIView):
    """
    Clase AdministradorList, lista todas los Administradores de las Empresas.
    Esta clase hereda de ListCreateAPIView, provee un método GET
    que Lista todos los Administradores.
    Nota: Solo usuarios com permiso Staff pueden consumirla.
    """
    permission_classes = (isSuperAdmin, )
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializers


class AdministradorDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializers


class AdministradorDetailUser(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Administrador.objects.filter(id_usuario=self.kwargs["pk_user"])
        return queryset
    serializer_class = AdministradorSerializers


class AdministradorUpdate(generics.UpdateAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Administrador.objects.all()
    lookup_field = 'pk'
    serializer_class = AdministradorSerializers


class AdministradoresViewSet(viewsets.ModelViewSet):
    """
    Filtro para precargar informacion de Administradores
    por E-Mail/first_name/last_name/celular.
    """
    permission_classes = [IsAuthenticated, isAdmin | isEmployee]
    serializer_class = AdministradoresFindSerializer

    def get_queryset(self):
        queryset = Administrador.objects.filter(id_empresa=self.kwargs["id_company"], id_usuario__is_active=True)
        return queryset


class AreaListAll(generics.ListCreateAPIView):
    """
    Clase AreaListAll, lista todas las Áreas de todas las Empresas.
    Esta clase hereda de ListCreateAPIView, provee un método GET
    que Lista todos los Administradores.
    Nota: Solo usuarios com permiso Staff pueden consumirla.
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = AreaSerializers

    def get_queryset(self):
        print("ROLLLL!!!!!!!!!")
        user = self.request.user
        print(user.roll)
        queryset = None
        if user.is_staff:
            queryset = Area.objects.all()
        else:
            if user.roll == settings.ADMIN or user.roll == settings.PROVIDER_ADMIN:
                try:
                    admin_company = Administrador.objects.get(id_usuario=user)
                except ObjectDoesNotExist:
                    return None
                # admin_company = Administrador.objects.filter(id_usuario=user)[0]
                id_company = admin_company.id_empresa
                queryset = Area.objects.filter(id_empresa=id_company)
            elif user.roll == settings.EMPLEADO:
                employeCompany = Empleado.objects.get(id_usuario=user)
                # admin_company = Empleado.objects.filter(id_usuario=user)[0]
                id_company = employeCompany.id_empresa
                print("id Company = " + str(id_company))
                queryset = Area.objects.filter(id_empresa=id_company)
            elif user.roll == settings.VIGILANTE:
                try:
                    guard_company = Vigilante.objects.get(id_usuario=user)
                except ObjectDoesNotExist:
                    return None
                id_company = guard_company.id_empresa
                queryset = Area.objects.filter(id_empresa=id_company)
        return queryset


class AreaDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, isAdmin|isAdminProvider]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Area.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            print("id Company = " + str(id_company))
            queryset = Area.objects.filter(id_empresa=id_company)
        return queryset
    serializer_class = AreaSerializers


class AreaUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, isAdmin|isAdminProvider]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Area.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            print("id Company = " + str(id_company))
            queryset = Area.objects.filter(id_empresa=id_company)
        return queryset
    lookup_field = 'pk'
    serializer_class = AreaSerializers


class VigilanteListAll(generics.ListCreateAPIView):
    permission_classes = (isAdmin, )
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Vigilante.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            print("id Company = " + str(id_company))
            queryset = Vigilante.objects.filter(id_empresa=id_company)
        return queryset
    serializer_class = VigilanteSerializers


class VigilanteDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isAdmin, )
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Vigilante.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            print("id Company = " + str(id_company))
            queryset = Vigilante.objects.filter(id_empresa=id_company)
        return queryset
    serializer_class = VigilanteSerializers


class VigilanteDetailUser(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Vigilante.objects.filter(id_usuario=self.kwargs["pk_user"])
        return queryset
    serializer_class = VigilanteSerializers


class VigilanteUpdate(generics.UpdateAPIView):
    permission_classes = (isAdmin, )

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Vigilante.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            print("id Company = " + str(id_company))
            queryset = Vigilante.objects.filter(id_empresa=id_company)
        return queryset
    lookup_field = 'pk'
    serializer_class = VigilanteSerializers


class EmpleadoListAll(generics.ListCreateAPIView):
    """List all avaiable employees of the administrator company.
    This only list all employees that belongs to the company wich the adm
    """
    permission_classes = (IsAuthenticated, isAdmin | isGuard | isAdminProvider,)  # Validates if this user is and Admin of some company
    serializer_class = EmpleadoSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Empleado.objects.all()
        else:
            if user.roll == settings.ADMIN or user.roll==settings.PROVIDER_ADMIN:
                admin_company = Administrador.objects.filter(id_usuario=user)[0]
                id_company = admin_company.id_empresa
                queryset = Empleado.objects.filter(id_empresa=id_company)
            else:
                if user.roll == settings.VIGILANTE:
                    vigilante_company = Vigilante.objects.filter(id_usuario=user)[0]
                    id_company = vigilante_company.id_empresa
                    queryset = Empleado.objects.filter(id_empresa=id_company)
        return queryset


class EmpleadoEmpresaXArea(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        Método que devuelve los Empleados de un Área Específica de una Empresa
        :return: Empleados de un Área Específica de una Empresa
        """
        queryset = Empleado.objects.filter(id_empresa=self.kwargs["pk"], id_area=self.kwargs["pk_area"])
        return queryset
    serializer_class = EmpleadoSerializers


class EmpleadoDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isAdmin, )
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Empleado.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            queryset = Empleado.objects.filter(id_empresa=id_company)
        return queryset
    serializer_class = EmpleadoSerializers


class EmpleadoDetailUser(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        queryset = Empleado.objects.filter(id_usuario=self.kwargs["pk_user"])
        return queryset
    serializer_class = EmpleadoSerializers


class EmpleadoUpdate(generics.UpdateAPIView):
    permission_classes =  [IsAuthenticated, IsAdmin|isAdminProvider]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Empleado.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            queryset = Empleado.objects.filter(id_empresa=id_company)
        return queryset
    lookup_field = 'pk'
    serializer_class = EmpleadoSerializers


class EmpleadosViewSet(viewsets.ModelViewSet):
    """
    Filtro para precargar informacion de Empleados.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmpleadosFindSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^id_usuario__celular', '^id_usuario__email']

    def get_queryset(self):
        user = self.request.user
        admin_company = Administrador.objects.filter(id_usuario=user)[0]
        id_company = admin_company.id_empresa
        queryset = Empleado.objects.filter(id_empresa=id_company, id_usuario__is_active=True)
        return queryset


class CasetaListAll(generics.ListCreateAPIView):
    permission_classes = (isAdmin | isGuard, )
    serializer_class = CasetaSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Caseta.objects.all()
        else:
            if user.roll == settings.ADMIN:
                admin_company = Administrador.objects.filter(id_usuario=user)[0]
                id_company = admin_company.id_empresa
                queryset = Caseta.objects.filter(id_empresa=id_company)
            else:
                if user.roll == settings.VIGILANTE:
                    guard_company = Vigilante.objects.filter(id_usuario=user)[0]
                    id_company = guard_company.id_empresa
                    queryset = Caseta.objects.filter(id_empresa=id_company)
        return queryset


class CasetaDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isAdmin, )
    serializer_class = CasetaSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Caseta.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            queryset = Caseta.objects.filter(id_empresa=id_company)
        return queryset

class CasetaUpdate(generics.UpdateAPIView):
    permission_classes = (isAdmin, )
    serializer_class = CasetaSerializers

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Caseta.objects.all()
        else:
            admin_company = Administrador.objects.filter(id_usuario=user)[0]
            id_company = admin_company.id_empresa
            queryset = Caseta.objects.filter(id_empresa=id_company)
        return queryset
    lookup_field = 'pk'


class AccesoList(generics.ListCreateAPIView):
    permission_classes = (isAdmin, )
    queryset = Acceso.objects.all()
    serializer_class = AccessSerializer

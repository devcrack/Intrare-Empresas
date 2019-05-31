from rest_framework import generics
from rest_framework import viewsets
from .serializers import *
from Usuarios.permissions import *
from Usuarios.models import CustomUser


class EmpresaList(generics.ListCreateAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isSuperAdmin, )
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


class AdministradorList(generics.ListCreateAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializers


class AdministradorDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializers


class AdministradorUpdate(generics.UpdateAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Administrador.objects.all()
    lookup_field = 'pk'
    serializer_class = AdministradorSerializers


class AreaListAll(generics.ListCreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializers


class AreaList(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        Método que devuelve las Áreas de una Empresa específica
        :return: Áreas de la Empresa
        """
        queryset = Area.objects.filter(id_empresa=self.kwargs["pk"])
        return queryset
    serializer_class = AreaSerializers


class AreaDetail(generics.RetrieveDestroyAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializers


class AreaUpdate(generics.UpdateAPIView):
    queryset = Area.objects.all()
    lookup_field = 'pk'
    serializer_class = AreaSerializers


class VigilanteListAll(generics.ListCreateAPIView):
    queryset = Vigilante.objects.all()
    serializer_class = VigilanteSerializers


class VigilanteList(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        Método que devuelve los Vigilantes de una Empresa específica
        :return: Vigilantes de la Empresa
        """
        queryset = Vigilante.objects.filter(id_empresa=self.kwargs["pk"])
        return queryset
    serializer_class = VigilanteSerializers


class VigilanteDetail(generics.RetrieveDestroyAPIView):
    queryset = Vigilante.objects.all()
    serializer_class = VigilanteSerializers


class VigilanteUpdate(generics.UpdateAPIView):
    queryset = Vigilante.objects.all()
    lookup_field = 'pk'
    serializer_class = VigilanteSerializers


class EmpleadoListAll(generics.ListCreateAPIView):
    """List all avaiable employees of the administrator company.

    """
    permission_classes = (is_admin,)  # Validates if this user is and Admin of some company
    serializer_class = EmpleadoSerializers

    def get_queryset(self):
        user = self.request.user
        admin_company = Administrador.objects.filter(id_usuario=user)[0]
        id_company = admin_company.id_empresa
        queryset = Empleado.objects.filter(id_empresa=id_company)

        return queryset

class EmpleadoList(generics.ListCreateAPIView):
    def get_queryset(self):
        """
        Método que devuelve los Empleados de una Empresa específica
        :return: Empleados de la Empresa
        """
        queryset = Empleado.objects.filter(id_empresa=self.kwargs["pk"])
        return queryset
    serializer_class = EmpleadoSerializers


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
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializers


class EmpleadoUpdate(generics.UpdateAPIView):
    queryset = Empleado.objects.all()
    lookup_field = 'pk'
    serializer_class = EmpleadoSerializers

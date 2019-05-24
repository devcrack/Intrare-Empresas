from rest_framework import generics
from .serializers import *


class EmpresaList(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaDetail(generics.RetrieveDestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaUpdate(generics.UpdateAPIView):
    queryset = Empresa.objects.all()
    lookup_field = 'pk'
    serializer_class = EmpresaSerializers


class AdministradorList(generics.ListCreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializers


class AdministradorDetail(generics.RetrieveDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializers


class AdministradorUpdate(generics.UpdateAPIView):
    queryset = Administrador.objects.all()
    lookup_field = 'pk'
    serializer_class = AdministradorSerializers

class EmpleadoList(generics.ListCreateAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializers


class EmpleadoDetail(generics.RetrieveDestroyAPIView):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializers


class EmpleadoUpdate(generics.UpdateAPIView):
    queryset = Empleado.objects.all()
    lookup_field = 'pk'
    serializer_class = EmpleadoSerializers

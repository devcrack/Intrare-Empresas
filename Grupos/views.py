from rest_framework import generics
from .serializers import *
from Usuarios.permissions import *
from Usuarios.models import CustomUser
from rest_framework.response import Response
from rest_framework import status


class GrupoDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isEmployee,)
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializers


class GrupoList(generics.ListCreateAPIView):
    permission_classes = (isEmployee,)
    serializer_class = GrupoSerializers

    def get_queryset(self):
        id_user = self.request.user.id
        employee = Empleado.objects.filter(id_usuario=id_user)[0]
        queryset = Grupo.objects.filter(id_empleado=employee)
        return queryset

    def create(self, request, *args, **kwargs):
        id_user = self.request.user.id
        employee = Empleado.objects.filter(id_usuario=id_user)[0]
        request.data['id_empleado'] = employee.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GrupoDelete(generics.DestroyAPIView):
    permission_classes = (isEmployee,)
    serializer_class = GrupoSerializers
    lookup_field = 'pk'
    queryset = Grupo.objects.all()


class GrupoUpdate(generics.UpdateAPIView):
    permission_classes = (isEmployee,)
    queryset = Grupo.objects.all()
    lookup_field = 'pk'
    serializer_class = GrupoSerializers

    def put(self, request, *args, **kwargs):
        id_user = self.request.user.id
        employee = Empleado.objects.filter(id_usuario=id_user)[0]
        request.data['id_empleado'] = employee.id
        print(request.data)
        return self.update(request, *args, **kwargs)


class ContactosXGrupoList(generics.ListAPIView):
    permission_classes = (isEmployee,)
    serializer_class = ContactosXGrupoSerializers

    def get_queryset(self):
        queryset = Grupo_has_contacto.objects.filter(id_grupo=self.kwargs['id_grupo'])
        return queryset


class ContactosXGrupoCreate(generics.CreateAPIView):
    permission_classes = (isEmployee,)
    serializer_class = ContactosXGrupoSerializersCreate

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContactosXGrupoDelete(generics.DestroyAPIView):
    permission_classes = (isEmployee,)
    serializer_class = ContactosXGrupoSerializersCreate
    lookup_field = 'pk'
    queryset = Grupo_has_contacto.objects.all()

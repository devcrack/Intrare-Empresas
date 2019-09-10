from rest_framework import generics
from .serializers import *
from Usuarios.permissions import *
from rest_framework.response import Response
from rest_framework import status


class ContactoList(generics.ListCreateAPIView):
    permission_classes = (isEmployee,)
    serializer_class = ContactoSerializers

    # def list(self, request, *args, **kwargs):
    #     id_user = self.request.user.id
    #     employee = Empleado.objects.filter(id_usuario=id_user)[0]
    #     # queryset = self.filter_queryset(self.get_queryset())
    #     contactos = Contacto.objects.filter(id_empleado=employee)
    #     queryset = contactos
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


    def get_queryset(self):
        id_user = self.request.user.id
        employee = Empleado.objects.filter(id_usuario=id_user)[0]
        queryset = Contacto.objects.filter(id_empleado=employee)
        return queryset

    def create(self, request, *args, **kwargs):
        id_user = self.request.user.id
        employee = Empleado.objects.filter(id_usuario=id_user)[0]
        # contacto = Contacto.objects.create(
        #     id_empleado=employee,
        #     nombre=self.request.data['nombre'],
        #     email=self.request.data['email'],
        #     telefono=self.request.data['telefono'],
        # )
        # contacto.save()
        request.data['id_empleado'] = employee.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContactoDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isEmployee,)
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializers


class ContactoUpdate(generics.UpdateAPIView):
    permission_classes = (isEmployee,)
    queryset = Contacto.objects.all()
    lookup_field = 'pk'
    serializer_class = ContactoSerializers

    def put(self, request, *args, **kwargs):
        id_user = self.request.user.id
        employee = Empleado.objects.filter(id_usuario=id_user)[0]
        request.data['id_empleado'] = employee.id
        print(request.data)
        return self.update(request, *args, **kwargs)


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

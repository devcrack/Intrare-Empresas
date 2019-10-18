from rest_framework import generics
from .serializers import *
from Usuarios.permissions import *
from Usuarios.models import CustomUser
from rest_framework.response import Response
from rest_framework import status


class GrupoDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isEmployee | isAdmin,)
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializers


class GrupoList(generics.ListCreateAPIView):
    permission_classes = (isEmployee | isAdmin,)
    serializer_class = GrupoSerializers

    def get_queryset(self):
        id_user = self.request.user.id
        queryset = Grupo.objects.filter(id_usuario=id_user)
        return queryset

    def create(self, request, *args, **kwargs):
        id_user = self.request.user.id
        request.data['id_usuario'] = id_user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GrupoDelete(generics.DestroyAPIView):
    permission_classes = (isEmployee | isAdmin,)
    serializer_class = GrupoSerializers
    lookup_field = 'pk'
    queryset = Grupo.objects.all()


class GrupoUpdate(generics.UpdateAPIView):
    permission_classes = (isEmployee | isAdmin,)
    queryset = Grupo.objects.all()
    lookup_field = 'pk'
    serializer_class = GrupoSerializers

    def put(self, request, *args, **kwargs):
        id_user = self.request.user.id
        request.data['id_usuario'] = id_user
        print(request.data)
        return self.update(request, *args, **kwargs)


class ContactosXGrupoList(generics.ListAPIView):
    permission_classes = (isEmployee | isAdmin,)
    serializer_class = ContactosXGrupoSerializers

    def get_queryset(self):
        queryset = Grupo_has_contacto.objects.filter(id_grupo=self.kwargs['id_grupo'])
        return queryset


class ContactosXGrupoCreate(generics.CreateAPIView):
    permission_classes = (isEmployee | isAdmin,)
    serializer_class = ContactosXGrupoSerializersCreate

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContactosXGrupoDelete(generics.DestroyAPIView):
    permission_classes = (isEmployee | isAdmin,)
    serializer_class = ContactosXGrupoSerializersCreate

    def destroy(self, request, *args, **kwargs):
        id_grupo = self.kwargs['id_grupo']
        id_user = self.kwargs['id_user']
        cont = Grupo_has_contacto.objects.filter(id_contacto=id_user, id_grupo=id_grupo)
        self.perform_destroy(cont)
        return Response(status=status.HTTP_204_NO_CONTENT)



from rest_framework import generics
from .serializers import *
from Usuarios.permissions import *
from rest_framework.response import Response
from rest_framework import status


class ContactoList(generics.ListCreateAPIView):
    permission_classes = (isEmployee,)
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializers

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
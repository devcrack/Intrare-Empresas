from rest_framework import generics
from .serializers import *
from Usuarios.permissions import *


class ContactoList(generics.ListCreateAPIView):
    permission_classes = (isEmployee,)
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializers


class ContactoDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isEmployee,)
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializers


class ContactoUpdate(generics.UpdateAPIView):
    permission_classes = (isEmployee,)
    queryset = Contacto.objects.all()
    lookup_field = 'pk'
    serializer_class = ContactoSerializers
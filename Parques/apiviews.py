from rest_framework import generics
from .serializers import *
from Usuarios.permissions import *


class ParqueList(generics.ListCreateAPIView):
    permission_classes = (isSuperAdmin,)
    queryset = Parque.objects.all()
    serializer_class = ParqueSerializers


class ParqueDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Parque.objects.all()
    serializer_class = ParqueSerializers


class ParqueUpdate(generics.UpdateAPIView):
    permission_classes = (isSuperAdmin, )
    queryset = Parque.objects.all()
    lookup_field = 'pk'
    serializer_class = ParqueSerializers
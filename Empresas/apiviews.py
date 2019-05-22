from rest_framework import generics
from .models import Empresa
from .serializers import EmpresaSerializers


class EmpresaList(generics.ListCreateAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers


class EmpresaDetail(generics.RetrieveDestroyAPIView):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers

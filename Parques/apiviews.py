from rest_framework import generics
from rest_framework import viewsets
from .serializers import *


class ParqueList(generics.ListCreateAPIView):

    #permission_classes = pass

    queryset = Parque.objects.all()
    serializer_class = ParqueSerializer
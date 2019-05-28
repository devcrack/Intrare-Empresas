from rest_framework import generics
from rest_framework import viewsets

from .serializers import *


class Invitacion_List(generics.ListCreateAPIView):
    """Invitacion_List list all available invitations.

    Class that evidently extends from ListCreateAPIView.
    ListCreateAPIView is used for read-only endpoints to represent a collection of
    model instances. This automatically provides a get method handler.
    """
    queryset = Invitacion.objects.all()  # Used for return objects from this view.
    serializer_class = InvitacionSerializers  # Used for validate and deserializing input, and for serializing output.

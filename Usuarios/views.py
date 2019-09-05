from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .permissions import *

from django.shortcuts import render

# Create your views here.


class UserPlatformCreateOrList(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPlatformSerializer


class UserUpdateParcial(generics.UpdateAPIView):
    """
    TIPO peticion: PATCH

    URLHost/UserPlatformUpdate/
    Header: Authorization Token #"$
    {
        "email": "newValue",
        "username": "newValue",
        "first_name": "newValue",
        "last_name": "newValue",
        "celular": newValue
    }
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        instance.email = request.data.get('email')
        instance.celular = request.data.get('celular')
        instance.username = request.data.get('username')
        instance.first_name = request.data.get('first_name')
        instance.last_name = request.data.get('last_name')

        # Performing Update
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class UserPasswordUpdate(generics.UpdateAPIView):
    """
        TIPO peticion: PATCH

        URLHost/UserPlatformUpdate/
        Header: Authorization Token #"$
        {
            "password": "newValue"
        }
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        newPassword = request.data.get('password')
        instance.set_password(newPassword)
        # Performing Update
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)

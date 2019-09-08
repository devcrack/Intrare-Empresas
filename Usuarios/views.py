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

    Realiza un update parcialmente a un determinado Usuario. El usuario lo obtenemos desde el request
    ya que este viene autentificado, de otra manera es imposible realizar la peticion.
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        _email = request.data.get('email')
        _numberPhone = request.data.get('celular')
        _set = CustomUser.objects.filter(email=_email)
        if len(set) > 0: # Determinamos si algun usuario ya tiene el correo electronico con el que se desea actualizar
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        _set = CustomUser.objects.filter(celular=_numberPhone)
        if len(set) > 0: # Determinamos si algun usuario ya tiene el numero celular con el que se desea actualizar
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
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

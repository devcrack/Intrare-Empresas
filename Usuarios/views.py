from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework import filters

from .serializers import *
from .permissions import *


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomFindSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^celular', '^email']


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
    Realiza update parcialmente a un determinado Usuario. El usuario se obtiene desde el request
    si es que esta autentificado.
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        _email = request.data.get('email')
        _numberPhone = request.data.get('celular')
        _set = CustomUser.objects.filter(email=_email)
        if len(_set) > 0: # Determinamos si algun usuario ya tiene el correo electronico con el que se desea actualizar
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'Error': 'El Email ya existe'})
        _set = CustomUser.objects.filter(celular=_numberPhone)
        if len(_set) > 0: # Determinamos si algun usuario ya tiene el numero celular con el que se desea actualizar
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'Error': 'El numero de movíl ya existe'})
        instance.email = request.data.get('email')
        instance.celular = request.data.get('celular')
        instance.username = request.data.get('username')
        instance.first_name = request.data.get('first_name')
        instance.last_name = request.data.get('last_name')

        # Performing Update
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)


# class UserUpdateByTemporalToken(generics.UpdateAPIView):
#
#
#     def update(self, request, *args, **kwargs):
#         _temporalToken = request.data.get('tToken')
#         _set = CustomUser.objects.filter(temporalToken=_temporalToken)
#         _setLen = len(_set)
#         if _setLen != 1:
#             return Response(status=status.HTTP_304_NOT_MODIFIED, data={'error':'Error con el tokenTemporal'})
#


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


class UserImgUpdate(generics.UpdateAPIView):
    """
    Actualizacion de imagenes de usuario IneFrente y Atras.
    Tipo de Peticion : PATCH.
    Header :
        - multipart/form-data
        - Authorization Token #"$
    Body Content:
        imgFront: 'pathFile'
        imgBack: 'pathFile'
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateIneSerializser
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            instance = self.request.user
            _imageFieldFront = _serializer.validated_data['imgFront']
            instance.ine_frente = _imageFieldFront
            instance.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)


class UserAvatarUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        self.serializer_class = UpdateOneIMGSerializser
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            instance = self.request.user
            _img = _serializer.validated_data['img']
            instance.avatar = _img
            instance.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)


class UserHaveIne(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instance = self.request.user
        ine = instance.ine_frente
        if not ine:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'warning': 'Usuario sin imagen INE Frente'})
        return Response(status=status.HTTP_200_OK)


class UpdateUserPartialByToken(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'temporalToken'
    serializer_class = CustomUserSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import UpdateModelMixin
from rest_framework import filters
from django.core.exceptions import ObjectDoesNotExist
# from django.conf import settings

from ControlAccs.utils import send_sms
from .serializers import *
from .permissions import *
from Empresas.models import Empleado, Administrador

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    Filtro para precargar informacion de un usuario.
    """
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomFindSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^celular', '^email']


class UserPlatformCreateOrList(generics.CreateAPIView):
    """
    Vista para crear un Usuario de la plataforma desde 0.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserPlatformSerializer
    lookup_field = "pk"

class UserUpdateParcial(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerilizerAPP

    def patch(self, request, *args, **kwargs):
        val = self.partial_update(request, *args, **kwargs)

        return val




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


class getUserByToken(generics.ListAPIView):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(temporalToken=self.kwargs['temporalToken'])
        return queryset


class activateUser(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee]  # Solo un Administrador o un Empleado pueden validar Invitados

    def update(self, request, *args, **kwargs):
        usr = self.request.user
        usrToken = request.data.get("usrToken")


        # usrToken = self.kwargs['temporalToken']

        instance = CustomUser.objects.filter(temporalToken=usrToken) # Buscamos al usuario a validar.
        if len(instance) != 1:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error:El token de usuario ha sido corrompido'})
        instance = instance[0]
        _tmpPassword = token_hex(3)  # Generamos su contraseña temporal
        instance.set_password(_tmpPassword) # Se establece contraseña temporal del usuario.
        instance.is_active = True # Activamos el usuario.
        instance.temporalToken=""  # Limpiamos su token Temporal.
        instance.save()
        #  Envio de invitacion0 y contraseña.
        addressee = instance.email
        if usr.roll == settings.ADMIN:
            _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
            _invs = Invitacion.objects.filter(id_usuario=instance, id_admin=_admCompany)
        else:
            employee = Empleado.objects.filter(id_usuario=usr)[0]
            _invs = Invitacion.objects.filter(id_usuario=instance, id_empleado=employee)
        _nInvs = len(_invs)
        if _nInvs> 0:
            # def validateDateInv(value):  #Se prevee solo enviar las invitacion en tiempo, es decir que no estan caducas
            #     _date = date(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day)
            #     if _date > value:
            #         raise serializers.ValidationError("La fecha de la invitacion esta vencida")

            _inv = _invs[_nInvs - 1] #Enviamos la ultima invitacion.
            _company = _inv.id_empresa.name
            _dateTime = str(_inv.dateInv) + " " + str(_inv.timeInv)
            _qrCode = _inv.qr_code
            _cellNumber = instance.celular
            html_message = render_to_string('passwordMail.html',
                                            {
                                                'empresa': _company,
                                                'fecha': _dateTime,
                                                'codigo': _qrCode,
                                                'password': _tmpPassword
                                            })
            send_IntrareEmail(html_message, addressee)  # MAIL
            _msgInv = "Se te ha enviado una invitación, verifica desde tu correo electrónico o en la aplicacion"
            _smsResponse = send_sms(_cellNumber, _msgInv)  # SMS
            if _smsResponse["messages"][0]["status"] == "0":
                log = 'Mensaje SMS ENVIADO'
            else:
                log = f"Error: {_smsResponse['messages'][0]['error-text']} al enviar SMS"
            print('LOGs SMS!! ')
            print(log)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT, data={'error:Error Inesperado'})
        return Response(status=status.HTTP_200_OK)





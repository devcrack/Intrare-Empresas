from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import date
from fcm_django.models import FCMDevice


from ControlAccs.utils import send_sms
from .serializers import *
from .permissions import *
from Invitaciones.models import Invitacion, InvitationByUsers
from django.db.models import Q

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    Filtro para precargar informacion de un usuario.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomFindSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^celular', '^email']

    def get_queryset(self):
        return CustomUser.objects.exclude(Q(id=self.request.user.id) | Q(is_active=False))


class UserPlatformCreateOrList(generics.CreateAPIView):
    """
    Vista para crear un Usuario de la plataforma desde 0.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserPlatformSerializer


class UserUpdateParcial(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]


    queryset = CustomUser.objects.all()
    lookup_field = "pk"
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

####DESHABILITADO ENVIO DE MENSAJES
class activateUser(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee]  # Solo un Administrador o un Empleado pueden validar Invitados

    def update(self, request, *args, **kwargs):
        usr = self.request.user
        usrToken = request.data.get("usrToken")

        try:
            instance = CustomUser.objects.get(temporalToken=usrToken)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'El token de usuario ha sido corrompido'})
        _tmpPassword = token_hex(3)  # tmp PASS
        instance.set_password(_tmpPassword)  # Se establece contraseña temporal del usuario.
        instance.is_active = True  # Activamos el usuario.
        instance.temporalToken = ""  # Limpiamos su token Temporal.
        instance.save()

        #  Envio de invitacion0 y contraseña.
        addressee = instance.email # Destinatario
        _userDevice = FCMDevice.objects.filter(user=instance)
        _invSByUSR = InvitationByUsers.objects.filter(host=usr, idGuest=instance)
        _currentDate = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                     day=timezone.datetime.now().day)  # Fecha actual
        index = 0
        for _invByUSR in _invSByUSR:
            _idInv = _invByUSR.idInvitation
            _inv = None
            try:
                _inv = Invitacion.objects.get(id=_idInv.id)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'error': 'ERROR EN INVITACION'})
            if _inv.dateInv >= _currentDate:
                _company = _inv.id_empresa.name
                _dateTime = str(_inv.dateInv) + " " + _inv.timeInv.strftime("%H:%M")
                _qrCode = _inv.qr_code
                _cellNumber = instance.celular
                _msgInv = "Se te ha enviado una invitacion, verifica desde tu correo electronico o en la aplicacion"
                html_message = render_to_string('FirstMailInv.html', {'empresa': _company, 'fecha': _dateTime,
                                                                      'codigo': _qrCode, 'password': _tmpPassword})
                if index == 0:
                    if len(_userDevice) > 0:
                        _userDevice.send_message(title="Intrare", body="Tienes una invitación", sound="Default") #PUSH
                    _smsResponse = send_sms(_cellNumber, _msgInv)  # SMS
                    if _smsResponse["messages"][0]["status"] == "0":
                        log = 'Mensaje SMS ENVIADO'
                    else:
                        log = f"Error: {_smsResponse['messages'][0]['error-text']} al enviar SMS"
                    print('LOGs SMS!! ')
                    print(log)
                print('Destinatario ', addressee)
                send_IntrareEmail(html_message, addressee)  # MAIL
                index += 1
        return Response(status=status.HTTP_200_OK)


class GetUsersNotActivated(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin | IsEmployee,)

    def get_queryset(self):
        usr = self.request.user
        queryset = CustomUser.objects.filter(host=usr)
        queryset = queryset.filter(is_active=False)
        return queryset

    def list(self, request, *args, **kwargs):
        _queryset = self.get_queryset()
        _nReg = len(_queryset)
        if _nReg > 0:
            _serializer= CustomFindSerializer(_queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteFMCUserDevice(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,]

    def delete(self, request, *args, **kwargs):
        _user = self.request.user
        # Obtener dispositivos de este usuario para eliminarlo.
        _userDevices = FCMDevice.objects.filter(user=_user)
        if len(_userDevices) > 0:
            _userDevices.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_302_FOUND, data={"Error": "Este Usuario no tiene dispositivos registrados"})

class RestorePasswordUser(generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        _userMail = request.data.get("email")
        print(_userMail)
        try:
            _usr = CustomUser.objects.get(email=_userMail)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Correo de usuario corrompido o inexistente"})
        _tmpPassword = token_hex(3)
        _usr.set_password(_tmpPassword)
        _userPhone = _usr.celular
        html_message = render_to_string('RestorePassword.html', {'password':_tmpPassword})
        send_IntrareEmail(html_message, _userMail)
        return Response(status=status.HTTP_200_OK)


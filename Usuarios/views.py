from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from datetime import date
from secrets import token_hex
from fcm_django.models import FCMDevice


from ControlAccs.utils import send_sms
from .serializers import *
from .permissions import *
from Invitaciones.models import Invitacion, InvitationByUsers
from Empresas.models import SecurityEquipment, Administrador, Empleado
from django.db.models import Q

# Create your views here.
#walletLink = 'https://api-intrare-development.herokuapp.com/wallet/create/'  # Development
walletLink = 'https://api-intrare-empresarial.herokuapp.com/wallet/create/'  # Production V1
linkConfirmAppointment = "https://api-intrare-empresarial.herokuapp.com/setConfirmed_AppointmentFromMail/" #Production V1
linkProvider = "https://first-project-vuejs.herokuapp.com/form_proveedor/"

def sendPushNotifies(idUser, msg):
    _userDevices = FCMDevice.objects.filter(user=idUser)
    if len(_userDevices) > 0:
        _userDevices.send_message(title="Intrare", body=msg, sound="Default")


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


class SimpleUserFilter(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, isAdmin]
    serializer_class = CustomFindSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^celular', '^email']

    def get_queryset(self):
        return CustomUser.objects.filter(is_active=True, roll=0)

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
    """
    Obtene un Usuario mediante su token.
    """
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.filter(temporalToken=self.kwargs['temporalToken'])
        return queryset

####DESHABILITADO ENVIO DE MENSAJES
class activateUser(generics.UpdateAPIView):
    """
    Activacion de un usuario cuando se ha confirmado su Identidad por parte del Anfitrion.
    Se envian todas sus invitaciones
    """
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
        instance.temporalToken = None  # Limpiamos su token Temporal.
        instance.save()

        #  Envio de invitacion y contraseña.
        _currentDate = timezone.datetime.now()
        addressee = instance.email # Destinatario
        _userDevice = FCMDevice.objects.filter(user=instance)
        _invitationSByUSR = InvitationByUsers.objects.filter(idInvitation__dateInv__gte=_currentDate, idGuest=instance)
        index = 0

        for _invByUSR in _invitationSByUSR:  # El usuario puede tener mas de una invitacion vinculada a su cuenta
            _idInv = _invByUSR.idInvitation
            _inv = None
            try:
                _inv = Invitacion.objects.get(id=_idInv.id)  # Obtenemos datos de la invitacion.
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'error': 'ERROR EN INVITACION'})
            # Aqui verificamos si la Invitacion es Valida, en base a su fecha.
            _walletLink = walletLink + _invByUSR.qr_code
            _company = _inv.id_empresa.name
            # _dateTime = str(_inv.dateInv) + " " + _inv.timeInv.strftime("%H:%M")
            _dateTime = str(_inv.dateInv) + " " + str(_inv.timeInv)
            _qrCode = _invByUSR.qr_code
            _cellNumber = instance.celular
            _idArea = _inv.id_area
            _typeInv = _inv.typeInv
            _secEqu_s = SecurityEquipment.objects.filter(idArea=_idArea)
            _securityEquipments = []
            for _SE in _secEqu_s:
                _securityEquipments.append(_SE.nameEquipment)
            _msgInv = "Se te ha enviado una invitacion, verifica desde tu correo electronico o en la aplicacion"
            _linkConfirm = linkConfirmAppointment + _qrCode + "/True/"
            html_message = render_to_string('FirstMailInv.html', {'empresa': _company, 'fecha': _dateTime,
                                                                  'codigo': _qrCode, 'password': _tmpPassword,
                                                                  'downloadFile': _walletLink,
                                                                  'secEqus': _securityEquipments,
                                                                  'linkConfirm': _linkConfirm,
                                                                  'typeInv': _typeInv})
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


class DeleteFMCUserDevice(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        _idDevice = request.data.get('idDevice')
        try:
            _device = FCMDevice.objects.get(registration_id=_idDevice)
        except(ObjectDoesNotExist, MultipleObjectsReturned):
            return Response(status=status.HTTP_409_CONFLICT, data={"error":"Su Dispositivo no Existe o se corrompio es decir "
                                                                           "existe mas de una vez en el origen de datos"})
        _device.delete()
        return Response(status=status.HTTP_200_OK)


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
        _usr.save()
        _userPhone = _usr.celular
        html_message = render_to_string('RestorePassword.html', {'password':_tmpPassword})
        send_IntrareEmail(html_message, _userMail)
        return Response(status=status.HTTP_200_OK)


class ActivateEmployee(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def update(self, request, *args, **kwargs):
        usr = self.request.user  # Administrador de Empresa.
        _employeeToken = request.data.get("usrToken")
        try:
            instance = CustomUser.objects.get(temporalToken=_employeeToken)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error" : "El token de usuario ha sido corrompido"})
        _tmpPassword = token_hex(3)
        instance.set_password(_tmpPassword)
        instance.is_active = True
        instance.temporalToken = None
        instance.save()

        addressee = instance.email
        _userDevice = FCMDevice.objects.filter(user=instance)
        _invitationSByUSR = InvitationByUsers.objects.filter(host=usr, idGuest=instance)

        _currentDate = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                            day=timezone.datetime.now().day)  # Fecha actual

        index = 0

        for _invByUSR in _invitationSByUSR:  # El Empleado puede tener mas de una invitacion vinculada a su cuenta
            _idInv = _invByUSR.idInvitation
            _inv = None
            try:
                _inv = Invitacion.objects.get(id=_idInv.id)  # Obtenemos datos de la invitacion.
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT, data={'error': 'ERROR EN INVITACION'})
            # Aqui verificamos si la Invitacion es Valida, en base a su fecha.
            if _inv.dateInv >= _currentDate:
                _walletLink = walletLink + _invByUSR.qr_code
                _company = _inv.id_empresa.name
                _dateTime = str(_inv.dateInv) + " " + _inv.timeInv.strftime("%H:%M")
                _qrCode = _invByUSR.qr_code
                _cellNumber = instance.celular
                _msgInv = "Se te ha enviado una invitacion, verifica desde tu correo electronico o en la aplicacion"
                html_message = render_to_string('FirstMailInv.html', {'empresa': _company, 'fecha': _dateTime,
                                                                      'codigo': _qrCode, 'password': _tmpPassword,
                                                                      'downloadFile': _walletLink})
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


class SendAlert(generics.ListAPIView):
    permission_classes = [IsAuthenticated, isAdmin | isEmployee]

    def get(self, request, *args, **kwargs):
        _user = self.request.user
        _idCompany = None

        if _user.roll is settings.ADMIN:
            try:
                _adminCompany = Administrador.objects.get(id_usuario=_user)
            except(ObjectDoesNotExist, MultipleObjectsReturned):
                return Response(status=status.HTTP_409_CONFLICT, data={"erro": "Usuario no Existente o existe multiples"
                                                                               "veces en el origen de datos. USUARIO "
                                                                               "CORROMPIDO"})
            _idCompany = _adminCompany.id_empresa
        else:
            try:
                _employee = Empleado.objects.get(id_usuario=_user)
            except(ObjectDoesNotExist, MultipleObjectsReturned):
                return Response(status=status.HTTP_409_CONFLICT, data={"erro": "Usuario no Existente o existe multiples"
                                                                               "veces en el origen de datos. USUARIO "
                                                                               "CORROMPIDO"})
            _idCompany = _employee.id_empresa

        _adminSet = Administrador.objects.filter(id_empresa=_idCompany)
        _employeeSet = Empleado.objects.filter(id_empresa=_idCompany)
        for admin in _adminSet:
            _idUser = admin.id_usuario
            sendPushNotifies(_idUser, "¡Alerta! ha Ocurrido una Incidencia Negativa en la Planta")
        for _employee in _employeeSet:
            _idUser = _employee.id_usuario
            sendPushNotifies(_idUser, "¡Alerta! ha Ocurrido una Incidencia Negativa en la Planta")

        return Response(status=status.HTTP_200_OK)


class DeleteEmployee(generics.DestroyAPIView):
    """"
    Downgrade Empleado -> Usuario Normal.
    Elimina un empleado de una determinada compañia, dejandolo solamente como un usuario normal.
    """
    permission_classes = [IsAuthenticated, isAdmin|isAdminProvider]

    def delete(self, request, *args, **kwargs):
        _currentUser = self.request.user
        try:
            admin = Administrador.objects.get(id_usuario=_currentUser)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Usuario de Administrador Corrompido"})
        _adminCompany = admin.id_empresa
        _idEmployee = self.kwargs["idEmployee"]
        try:
            _employee = Empleado.objects.get(id=_idEmployee)
        except(ObjectDoesNotExist, MultipleObjectsReturned):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Datos de empleado corrompidos"})
        _employeeCompany = _employee.id_empresa

        if _adminCompany.id is not _employeeCompany.id:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Intento de Eliminacion de Empleado de "
                                                                               "una empresa externa"})
        _idUser = _employee.id_usuario
        _idUser.roll = 0
        _idUser.save()
        _employee.delete()
        return Response(status=status.HTTP_200_OK)


class UpgradeUserToEmployee(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, isAdmin]

    def update(self, request, *args, **kwargs):
        _currentUser = self.request.user
        try:
            admin = Administrador.objects.get(id_usuario=_currentUser)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Usuario de Administrador Corrompido"})
        # <<<Se obtiene empresa, a partir del administrador logueado>>>
        _Company = admin.id_empresa

        # <<Datos JSON >>
        _idUser = int(request.data.get("idUsuario"))
        _idArea = int(request.data.get("idArea"))
        _extension = request.data.get("extension")
        try:
            _area = Area.objects.get(id_empresa=_Company, id=_idArea)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "No existe el area especificada"})
        try:
            _user = CustomUser.objects.get(id=_idUser)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "El usuario especificado no se existe"})
        _user.roll = 1
        _user.save()
        _nwEmployee = Empleado(id_empresa=_Company, id_usuario=_user, id_area=_area, extension=_extension)
        _nwEmployee.save()
        
        return Response(status=status.HTTP_200_OK)


class CreateProvider(generics.CreateAPIView):
    """Crea un provedor no Existente"""
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserSerilizerAPP
        # _pass = token_hex(3)
        # print("password Provedor " + _pass)
        _serializer = self.serializer_class(data=request.data, context={'user':request.user})
        if _serializer.is_valid():
            _serializer.save()
            self.sendMailNewProvider(_serializer.instance.temporalToken,
                                     _serializer.data['email'])
            print('FIN')
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)


    @classmethod
    def sendMailNewProvider(cls, tk, mail):
        _link = linkProvider + tk
        htmlMsg = render_to_string(
            "providerMail.html", {
                "link": _link
            })
        send_IntrareEmail(htmlMsg, mail)

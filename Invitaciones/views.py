from hmac import new

from django.db.utils import Error

# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from Usuarios.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from secrets import token_hex
from ControlAccs.utils import send_sms, send_IntrareEmail
from fcm_django.models import FCMDevice
from django.db.models import Q
from django.core.files.storage import default_storage
import re

_regexMail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
linkWallet = 'https://api-intrare-development.herokuapp.com/wallet/create/'
linkPreregisterUser = 'https://web-intrare.herokuapp.com/preregistro/'
linkPreregisterEmployee = "URL"

def guest_exist(cellphoneN, _email):
    if _email is None:
        try:
            user = CustomUser.objects.get(celular=cellphoneN)
        except ObjectDoesNotExist:
            return None
    else:
        try:
            user = CustomUser.objects.get(Q(email=_email) | Q(celular=cellphoneN))
        except ObjectDoesNotExist:
            return None
    return user


def create_user(_email, cellphone):
    _errorResponse = None

    
    if _email is None: # No se dio Ningun EMAIL
        nw_user = CustomUser(
            email=None, celular=cellphone, password='pass', username=cellphone, temporalToken=token_hex(4),
            is_active=False)
    else: # Se  ingreso un EMAIL
        _aEmail = _email.lower()
        nw_user = CustomUser( email=_aEmail, celular=cellphone, username=_aEmail,
                              temporalToken=token_hex(4), is_active=False)
        nw_user.set_password('mientras123')
    try:
        nw_user.save()
        print(nw_user.id, ' USER CREATED 200_OK')
    except ValueError:
        _errorResponse = {'Error': 'Error in User Create'}
    return _errorResponse, nw_user


def render_InvMail(_nameEmpresa, _dateInv, _qrCode, _wallet, _secEqus):
    html_message = render_to_string('email.html',
                                    {'empresa': _nameEmpresa,
                                     'fecha': _dateInv,
                                     'codigo': _qrCode,
                                     'downloadFile': _wallet,
                                     'secEqus': _secEqus})
    return html_message


def render_MsgPregister(_headerMsg, msg, link):
    html_message = render_to_string('nwUserMail.html',
                                    {'headerMsg': _headerMsg,
                                     'msg': msg,
                                     'link': link
                                     })
    return html_message


def justCreateInvitation(id_company, id_area, _typeInv, _dateInv, _timeInv, expDate,
                      subject, vehicle, notes, from_company, _diary):
    nw_invitation = Invitacion(
        id_empresa=id_company,
        id_area=id_area,
        dateInv=_dateInv,
        timeInv=_timeInv,
        asunto=subject,
        automovil=vehicle,
        notas=notes,
        expiration=expDate,
        empresa=from_company,
        typeInv=_typeInv,
        diary=_diary
    )
    nw_invitation.save()
    return nw_invitation


####DESHABILITADO ENVIO DE MENSAJES
def createOneMoreInvitaitons(id_company, id_area, _host, listGuest, typeInv, _dateInv, _timeInv, expDate,
                             subject, vehicle, notes, from_company, diary):
    error_response = None
    _mainMsg = 'Bienvenido a Intrare. '
    _msgReg = None
    _msgInv = None

    inv = justCreateInvitation(id_company, id_area, typeInv, _dateInv, _timeInv, expDate,
                               subject, vehicle, notes, from_company, diary)
    for _guest in listGuest:
        _email = _guest['email']
        print(_email)
        _cellphone = _guest['cellphone']
        print(_cellphone)
        _idUser = guest_exist(_cellphone, _email)  # Si el Usuario no existe, forzosamente proporcionar el Numero de celular y email.
        if _idUser == _host:
            error_response = {"error": "Una extraña sitaucion ha ocurrido. Estas ingresando tus propios datos en la invitacion"}
            return error_response, None
        if _idUser is None:
            error_response, _idUser = create_user(_email, _cellphone)
            if error_response:
                return error_response, None  # SE SALE ALV!
        # En este punto ya se obutvo o se hizo la creacion del INVITADO/USUARIO
        _idUser.host = _host
        _idUser.save()

        _specialQR = token_hex(8) + str(_idUser.id) # CONCATENADO
        _nwInByUSER = InvitationByUsers(idInvitation=inv, qr_code=_specialQR, host=_host, idGuest=_idUser)
        _nwInByUSER.save()

        if _idUser.is_active:  # El proceso de notificacion de Invitacion se realiza normalmente
            _secEqu_s = SecurityEquipment.objects.filter(idArea=id_area)
            _securityEquipments = []
            for _SE in _secEqu_s:
                _securityEquipments.append(_SE.nameEquipment)

            _userDevices = FCMDevice.objects.filter(user=_idUser)
            host_name = _host.first_name + _host.last_name
            _msgInv = "Se te ha enviado una invitacion, verifica desde tu correo electrónico o en la aplicacion"
            _dateTime = str(inv.dateInv) + " " + str(inv.timeInv)
            _wallet = linkWallet + _specialQR
            _htmlMessage = render_InvMail(inv.id_empresa.name, _dateTime,
                                          _nwInByUSER.qr_code, _wallet, _securityEquipments)
            if len(_userDevices) > 0:
                _userDevices.send_message(title="Intrare", body="Se te ha enviado una invitación. Anfitrion: " + host_name,
                                          sound="Default")
            send_IntrareEmail(_htmlMessage, _idUser.email)  # EMAIL
            _smsResponse = send_sms(_idUser.celular, _msgInv) #SMS
        # Se envia al usuario una notificacion para que realize su preRegistro N VECES
        else:
            _msgReg = "Recibiste una invitacion. Para acceder a ella realiza tu Preregistro en:"
            _link = linkPreregisterUser + str(_idUser.temporalToken) + '/'
            msg = _mainMsg + _msgReg + _link
            _smsResponse = send_sms(_idUser.celular, msg)  # SMS
            if _idUser.email:
                _htmlMessage = render_MsgPregister(_mainMsg, _msgReg, _link)
                send_IntrareEmail(_htmlMessage, _idUser.email)  # EMAIL
        if _smsResponse["messages"][0]["status"] == "0":
            log = 'Mensaje SMS ENVIADO'
        else:
            log = f"Error: {_smsResponse['messages'][0]['error-text']} al enviar SMS"
        print('LOGs SMS!! ')
        print(log)
        print(inv.id, ' INVITATION CREATED  200_OK')
    return error_response, inv


def validate_employee(_id_company, _id_employee):
    id_company = _id_company
    id_employee = _id_employee
    error_response = None
    employee = None
    employee_s = Empleado.objects.filter(id_empresa=id_company, id=id_employee)
    if employee_s:
        print('Employee FOUND!!!')
        employee = employee_s[0]
    else:
        print('Employee NOT FOUND')
        error_response = {'Error': 'El empleado no Existe'}
    return error_response, employee


def validate_areas(_id_company, _id_area):
    """
        Args:
            args[0]: Id_company.
            args[1]: area name.

        Returns:
            tuple:data error message and area if is found it.
    """
    id_company = _id_company
    id_area = _id_area
    area = None
    error_response = None

    area_s = Area.objects.filter(id_empresa=id_company, id=id_area)
    if area_s:
        area = area_s[0]
    else:
        error_response = {'Error': 'No existen areas con el Id proporcionado'}
    return error_response, area


def expDate(dateInv):
    exp = timezone.datetime.strptime(dateInv , "%Y-%m-%d").date()
    delta = timezone.timedelta(days=2)
    exp = exp + delta
    return exp

def dateInv():
    _year = timezone.datetime.now().year
    _month = timezone.datetime.now().month
    _day = timezone.datetime.now().day
    _date = date(_year, _month, _day)
    return _date

class InvitationListAdminEmployee(viewsets.ModelViewSet): ####
    permission_classes = [IsAuthenticated,IsAdmin | IsEmployee,]  # The user logged have to be and admin or an employee

    def list(self, request, *args, **kwargs):
        y = self.kwargs['year']
        m = self.kwargs['month']
        d = self.kwargs['day']
        usr = self.request.user

        invsByUser = InvitationByUsers.objects.filter(host=usr, idInvitation__fecha_hora_envio__year=y,
                                                      idInvitation__fecha_hora_envio__month=m,
                                                      idInvitation__fecha_hora_envio__day=d) # Todas las invitaciones que ha generado este Usuario.
        queryset = self.queryset = invsByUser
        # serializer = InvitationToHostSerializer(queryset, many=True) #Cagadas del Andres
        serializer = InvitationToGuardSerializer(queryset, many=True)
        return Response(serializer.data)


class InvitationListToGuard(viewsets.ModelViewSet): ####
    permission_classes = (isGuard,)

    def list(self, request, *args, **kwargs):
        qr_code = self.kwargs['qr_code']
        self.queryset = InvitationByUsers.objects.filter(qr_code=qr_code)

        # self.queryset = Invitacion.objects.filter(qr_code=qr_code)
        _nReg = len(self.queryset)
        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = InvitationToGuardSerializer(queryset, many=True, context={"request": request})
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationListToManagerAndEmployee(viewsets.ModelViewSet):
    """
        Vista para mostrar la Información de la Invitación por ID_INVITACION
    """
    permission_classes = (isEmployee | isAdmin,)

    def list(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        self.queryset = InvitationByUsers.objects.filter(id=pk)
        _nReg = len(self.queryset)
        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = InvitationToGuardSerializer(queryset, many=True, context={"request": request})
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationListToSimpleUser(viewsets.ModelViewSet): ####
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        _currentDate = timezone.datetime.now()
        _query = InvitationByUsers.objects.filter(idGuest=self.request.user.id)
        _query = _query.filter(idInvitation__dateInv__gte=_currentDate)
        _nReg = len(_query)
        if _nReg > 0:
            print('nReg=', _nReg)
            _serializer = InvitationToSimpleUserSerializer(_query, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class MassiveInvitationCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee, ]

    def create(self, request, *args, **kwargs):
        usr = self.request.user
        self.serializer_class = MasiveInvSerializer
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()

            _areaId = _serializer.data['areaId']
            _guests = _serializer.data['guests'] #Lista invitados 1 | +
            _dateInv = _serializer.data['dateInv']
            _timeInv = _serializer.data['timeInv']
            _exp = _serializer.data['exp']
            _subject = _serializer.data['subject']
            _vehicle = _serializer.data['vehicle']
            _notes = _serializer.data['notes']
            _companyFrom = _serializer.data['companyFrom']
            _typeInv = _serializer.data['typeInv']
            _diary = _serializer.data['diary']

            if _dateInv is None:
                _dateInv = dateInv()

            if _exp is None:
                _exp = expDate(str(_dateInv))

            if usr.roll == settings.ADMIN:
                _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
                _idCompany = _admCompany.id_empresa # Obtener ID_EMPRESA via ADMIN
            else:  # Logged as Employee
                _employee = Empleado.objects.filter(id_usuario=usr)[0]
                _idCompany = _employee.id_empresa  # Obtener ID_EMPRESA via EMPLEADO
            _errorResponse, _area = validate_areas(_idCompany, _areaId)  # Validando AREAS
            if _area:
            #  Creacion de Invitacion
                _errorResponse, invitation = createOneMoreInvitaitons(_idCompany, _area, usr, _guests,_typeInv,
                                                                      _dateInv, _timeInv, _exp, _subject,_vehicle,
                                                                      _notes, _companyFrom, _diary)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST) # Error al crear Invitacion
            else:
                return Response(data=_errorResponse, status=status.HTTP_404_NOT_FOUND)  # Error ID de Area
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)
        return Response(status=status.HTTP_201_CREATED, data=_serializer.data)


class InvitationbyQRCode(generics.ListAPIView):
    serializer_class = InvitationToGuardSerializer

    def get_queryset(self):
        queryset = InvitationByUsers.objects.all()
        # queryset = Invitacion.objects.all()
        _qrCode = self.kwargs['qrcode']
        if _qrCode is not None:
            queryset = queryset.filter(qr_code=_qrCode)
        return queryset


class GetInvitationByHOST(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsAdmin | IsEmployee, ]  # The user logged have to be and admin or an employee

    def list(self, request, *args, **kwargs):
        usr = self.request.user
        _queryset = self.queryset = InvitationByUsers.objects.filter(host=usr)
        serializers = InvitationToHostSerializer(_queryset, many=True)
        return Response(serializers.data)


# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


class Createreferredinvitation(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,IsAdmin | IsEmployee, ]  # The user logged have to be and admin or an employee

    def create(self, request, *args, **kwargs):
        self.serializer_class = ReferredInvitationSerializerCreate
        _serializer = self.serializer_class(data=request.data, context={'request': request})
        if _serializer.is_valid(raise_exception=True):
            _serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetReferredInv(viewsets.ModelViewSet):
    def get_queryset(self):
        try:
            _querySet = ReferredInvitation.objects.get(Token=self.kwargs['token'])
        except ObjectDoesNotExist:
            return None
        return _querySet

    def list(self, request, *args, **kwargs):
        _querySet = self.get_queryset()
        if _querySet is not None:
            _serializer = GetReferralInvSerializer(_querySet)
            return Response(status=status.HTTP_200_OK, data=_serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResendReferralInvitation(generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        _token = request.data.get("token")
        _newReferralMail = request.data.get("referralMail")
        if re.search(_regexMail, _newReferralMail):
            try:
                _referralInvitation = ReferredInvitation.objects.get(qrCode=_token)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_204_NO_CONTENT, data={"Error": "Token corrompido"})
            _numForwarding = _referralInvitation.maxForwarding
            _referralExpiration = _referralInvitation.referredExpiration
            if _numForwarding < 1:
                return Response(status=status.HTTP_403_FORBIDDEN, data={'error':'Se ha excedido el numero maximo de reenvios'})
            _currentDate = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                                day=timezone.datetime.now().day)  # Fecha actual
            if _referralInvitation < _currentDate:
                return Response(status=status.HTTP_403_FORBIDDEN,
                                data={'error': f'Esta peticion esta caducada: {_referralExpiration}'})
            _token = token_hex(7)  # Renovando Token.
            _numForwarding = _numForwarding - 1
            _referralInvitation.qrCode = _token
            _referralInvitation.maxForwarding = _numForwarding
            _referralInvitation.referredMail = _newReferralMail
            _referralInvitation.save()
            _link = "URL/"+_token
            html_message = render_to_string("referredMail.html",
                                            {
                                                "forwardNum": _numForwarding,
                                                "link": _link
                                            })
            send_IntrareEmail(html_message, _newReferralMail)
            return Response(status=status)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"Error": "Email Invalido"})


class CreateReferredInvitation(generics.CreateAPIView):
    """
    Este metodo solo sirve para crear un registro ReferredInvitation
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsEmployee, ]
    queryset = ReferredInvitation.objects.all()
    serializer_class = Createreferredinvitation


def justCreateEnterpriseInv(serializer, _host):
    error_response = None
    idCompany = serializer.data['id_empresa']
    idArea = serializer.data['areaId']
    dateInv = serializer.data['dateInv']
    timeInv = serializer.data['timeInv']
    expDate = serializer.data['expiration']
    subject = serializer.data['subject']
    vehicle = serializer.data['vehicle']
    notes = serializer.data['notes']
    _fromCompany = serializer.data['companyFrom']
    _idReferredInv = serializer.data['idReferredInv']
    _guestMail = serializer.data['guest']['email']
    _guestPhone = serializer.data['guest']['cellphone']
    _diary = serializer.data['diary']
    _company = Empresa.objects.get(id=idCompany)
    _area = Area.objects.get(id=idArea)
    try:
        _refInv = ReferredInvitation.objects.get(id=_idReferredInv)
    except ObjectDoesNotExist:
        error_response = {"error": "Esta invitación Referida no Existe Mas"}
        return error_response, None

    inv = justCreateInvitation(_company, _area, 1, dateInv, timeInv, expDate, subject, vehicle, notes,
                               _fromCompany, _diary)
    _idUser = guest_exist(_guestPhone, _guestMail)
    if _idUser == _host:
        error_response = {"error": "Una extraña sitaucion ha ocurrido. Estas ingresando tus propios datos en la invitacion"}
        return error_response, None
    if _idUser is None:
        print("PREREGISTRANDO USUARIO")
        error_response, _idUser = create_user(_guestMail, _guestPhone)
        if error_response:
            return error_response, None
    _idUser.host = _host
    _idUser.save()

    _specialQR = token_hex(8) + str(_idUser.id)
    _nwInByUSER = InvitationByUsers(idInvitation=inv, qr_code=_specialQR, host=_host, idGuest=_idUser)
    _nwInByUSER.save()
    if _idUser.is_active:
        _secEqu_s = SecurityEquipment.objects.filter(idArea=idArea)
        _securityEquipments = []
        for _SE in _secEqu_s:
            _securityEquipments.append(_SE.nameEquipment)
        _userDevices = FCMDevice.objects.filter(user=_idUser)
        host_name = _host.first_name + _host.last_name
        _msgInv = "Se te ha enviado una invitacion, verifica desde tu correo electrónico o en la aplicacion"
        _dateTime = str(inv.dateInv) + " " + str(inv.timeInv)
        _wallet = linkWallet + _specialQR
        _htmlMessage = render_InvMail(inv.id_empresa.name, _dateTime,
                                      _nwInByUSER.qr_code, _wallet, _securityEquipments)
        if len(_userDevices) > 0:
            _userDevices.send_message(title="Intrare", body="Se te ha enviado una invitación Empresarial. Anfitrion: " + host_name,
                                      sound="Default")
        send_IntrareEmail(_htmlMessage, _idUser.email)  # EMAIL
        _smsResponse = send_sms(_idUser.celular, _msgInv) #SMS
    else:  # Preregistro Empleado
        _msgReg = "Recibiste una invitacion Empresarial. Para acceder a ella realiza tu Preregistro en:"
        link = linkPreregisterEmployee
        link = link + _idUser.temporalToken + "/"
        _smsMSG = "Bienvenido a Intrare. " + _msgReg + link
        _smsResponse = send_sms(_idUser.celular, _smsMSG)  # SMS
        if _idUser.email:
            _htmlMessage = render_MsgPregister("Bienvenido a Intrare. ", _msgReg, link)
            send_IntrareEmail(_htmlMessage, _idUser.email)  # EMAIL
    if _smsResponse["messages"][0]["status"] == "0":
        log = 'Mensaje SMS ENVIADO'
    else:
        log = f"Error: {_smsResponse['messages'][0]['error-text']} al enviar SMS"
    print('LOGs SMS!! ')
    print(log)
    print(inv.id, ' INVITATION CREATED  200_OK')
    _refInv.delete()
    return error_response, inv


class CreateEnterpriseInvitation(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        # usr = self.request.user # REFERENCIADO. Persona encargada de cerrar la Invitacion.
        self.serializer_class = EnterpriseSerializer
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            _idHost = _serializer.data['host']
            try:
                _host = CustomUser.objects.get(id=_idHost)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"error" : "Error con su Cuenta de Administrador"})

            _errorResponse, invitation = justCreateEnterpriseInv(_serializer, _host)
            if _errorResponse:
                return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)  # Error al crear Invitacion
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)
        return Response(status=status.HTTP_201_CREATED, data=_serializer.data)


class DeleteInvitation(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,IsAdmin | IsEmployee,]

    queryset = Invitacion.objects.all()
    serializer_class = FullInvitationSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

















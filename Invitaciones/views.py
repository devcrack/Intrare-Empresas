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


def guest_exist(cellphoneN, _email):
    if _email is None:
        try:
            user = CustomUser.objects.get(celular=cellphoneN)
        except ObjectDoesNotExist:
            return None
    else:
        try:
            user = CustomUser.objects.get(email=_email, celular=cellphoneN)
        except ObjectDoesNotExist:
            return None
    return user


def create_user(_email, cellphone):
    _errorResponse = None
    if _email is None: # No se dio Ningun EMAIL
        nw_user = CustomUser(
            email=None, celular=cellphone, password='pass', username=cellphone, temporalToken=token_hex(4),
            is_active=False)
    else:
        _aEmail = _email.lower()
        nw_user = CustomUser( email=_aEmail, celular=cellphone, username=_aEmail, password='pass',
                              temporalToken=token_hex(4), is_active=False)
    try:
        nw_user.save()
        print(nw_user.id, ' USER CREATED 200_OK')
    except ValueError:
        _errorResponse = {'Error': 'Error in User Create'}
    return _errorResponse, nw_user


def render_InvMail(_nameEmpresa, _dateInv, _qrCode):
    html_message = render_to_string('email.html',
                                    {'empresa': _nameEmpresa,
                                     'fecha': _dateInv,
                                     'codigo': _qrCode}
                                    )
    return html_message


def render_MsgPregister(_headerMsg, msg, link):
    html_message = render_to_string('nwUserMail.html',
                                    {'headerMsg': _headerMsg,
                                     'msg': msg,
                                     'link': link
                                     })
    return html_message


def justCreateInvitation(id_company, id_area, _typeInv, _dateInv, _timeInv, expDate,
                      subject, vehicle, notes, from_company):
    error_response = None
    _mainMsg = 'Bienvenido a Intrare. '
    _msgReg = None
    _link = 'https://first-project-vuejs.herokuapp.com/preregistro/'
    _msgInv = None

    nw_invitation = Invitacion(
        id_empresa=id_company,
        id_area=id_area,
        dateInv=_dateInv,
        timeInv=_timeInv,
        expiration=expDate,
        asunto=subject,
        automovil=vehicle,
        notas=notes,
        empresa=from_company,
        typeInv=_typeInv
    )
    nw_invitation.save()
    return nw_invitation

####DESHABILITADO ENVIO DE MENSAJES
def createOneMoreInvitaitons(id_company, id_area, _host, listGuest, typeInv, _dateInv, _timeInv, expDate,
                             subject, vehicle, notes, from_company):
    error_response = None
    _mainMsg = 'Bienvenido a Intrare. '
    _msgReg = None
    _msgInv = None

    inv = justCreateInvitation(id_company, id_area, typeInv, _dateInv, _timeInv, expDate,
                               subject, vehicle, notes, from_company)
    for _guest in listGuest:
        _email = _guest['email']
        print(_email)
        _cellphone = _guest['cellphone']
        print(_cellphone)
        _idUser = guest_exist(_cellphone, _email)  # Si el Usuario no existe, forzosamente proporcionar el Numero de celular y email.
        if _idUser is None:
            error_response, _idUser = create_user(_email, _cellphone)
            if error_response:
                return error_response, None  # SE SALE ALV!
        # En este punto ya se obutvo o se hizo la creacion del INVITADO/USUARIO
        _idUser.host = _host
        _idUser.save()
        _nwInByUSER = InvitationByUsers(idInvitation=inv, qr_code= inv.qr_code, host=_host, idGuest=_idUser)  # Se da
        _nwInByUSER.save()  # de Alta al Usuario con su respectiva invitacion

        if _idUser.is_active:  # El proceso de notificacion de Invitacion se realiza normalmente
            _msgInv = "Se te ha enviado una invitacion, verifica desde tu correo electrónico o en la aplicacion"

            _dateTime = str(inv.dateInv) + " " + str(inv.timeInv)
            _htmlMessage = render_InvMail(inv.id_empresa.name, _dateTime,
                                          inv.qr_code)
            _smsResponse = send_sms(_idUser.celular, _msgInv)  # SMS.
            send_IntrareEmail(_htmlMessage, _idUser.email)  # EMAIL
        else:  # Se envia al usuario una notificacion para que realize su preRegistro N VECES
            _msgReg = "Recibiste una invitacion. Para acceder a ella realiza tu Pregistro en:"
            _link = 'https://first-project-vuejs.herokuapp.com/preregistro/'
            _link = _link + str(_idUser.temporalToken) + '/'
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


def validateSecEqu(listSecEq):
    _idSecEqList = []
    for i in listSecEq:
        if i != '':
            print(i)
            _idSecEq = int(i)
            try:
                _secEqu = EquipoSeguridad.objects.get(id=_idSecEq)
                _idSecEqList.append(_secEqu)
            except ObjectDoesNotExist:
                return None, {'Error': 'Error with Security Equipment supplied, please check it'}
    return _idSecEqList, None


def add_sec_equ_by_inv(list_equipment_security, inv):
    error_response = None
    for i in list_equipment_security:
        _eqInv = EquiposporInvitacion(id_equipo_seguridad=i, id_invitacion=inv)
        try:
            _eqInv.save()
            print('Equipment by Invitation Created 200_OK')
        except ValueError:
            error_response = {'Error': 'Can\'t create Equipment for invitation'}
            return error_response
    return error_response


def expDate(dateInv):
    exp = timezone.datetime.strptime(dateInv , "%Y-%m-%d").date()
    delta = timezone.timedelta(days=2)
    exp = exp + delta
    return exp


class EquipoSeguridadList(generics.ListCreateAPIView):
    """
    Clase AdministradorList, lista todas los Administradores de las Empresas.
    Esta clase hereda de ListCreateAPIView, provee un método GET
    que Lista todos los Administradores.
    Nota: Solo usuarios com permiso Staff pueden consumirla.
    """
    queryset = EquipoSeguridad.objects.all()
    serializer_class = EquipoSeguridadSerializers



class EquipoSeguridadXInvitacionList(generics.ListAPIView):
    def get_queryset(self):
        """
        Método que devuelve el equipo de Seguridad por Invitación
        :return: lista de equipos de seguridad
        """
        queryset = EquiposporInvitacion.objects.filter(id_invitacion=self.kwargs["id_invitation"])
        return queryset

    serializer_class = EquipoSeguridadXInvitacionSerializers



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


class InvitationListToSimpleUser(viewsets.ModelViewSet): ####
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = InvitationByUsers.objects.filter(idGuest=self.request.user.id)
        # self.queryset = Invitacion.objects.filter(id_usuario=self.request.user.id)
        _nReg = len(self.queryset)
        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = InvitationToSimpleUserSerializer(queryset, many=True)
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
            _listSecEquip = _serializer.data['secEquip']
            _guests = _serializer.data['guests'] #Lista invitados 1 | +
            _dateInv = _serializer.data['dateInv']
            _timeInv = _serializer.data['timeInv']
            _exp = _serializer.data['exp']
            _subject = _serializer.data['subject']
            _vehicle = _serializer.data['vehicle']
            _notes = _serializer.data['notes']
            _companyFrom = _serializer.data['companyFrom']
            _typeInv = _serializer.data['typeInv']

            _arraySecEquip = _listSecEquip.split(',')

            if _exp is None:
                _exp = expDate(_dateInv)
            if usr.roll == settings.ADMIN:
                _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
                _idCompany = _admCompany.id_empresa # Obtener ID_EMPRESA via ADMIN
            else:  # Logged as Employee
                _employee = Empleado.objects.filter(id_usuario=usr)[0]
                _idCompany = _employee.id_empresa  # Obtener ID_EMPRESA via EMPLEADO
            _errorResponse, _area = validate_areas(_idCompany, _areaId)  # Validando AREAS
            if _area:
                _securityEqu, _errorResponse = validateSecEqu(_arraySecEquip) # Validando equipo de seguridad
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_404_NOT_FOUND)
            #  Creacion de Invitacion
                _errorResponse, invitation = createOneMoreInvitaitons(_idCompany, _area, usr, _guests,_typeInv,
                                                                      _dateInv, _timeInv, _exp, _subject,_vehicle,
                                                                      _notes, _companyFrom)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST) # Error al crear Invitacion
                if _securityEqu:
                    _errorResponse = add_sec_equ_by_inv(_securityEqu, invitation)
                    if _errorResponse:
                        return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)  # Error al crear Invitacion
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
        _queryset = self.queryset =  InvitationByUsers.objects.filter(host=usr)
        serializers = InvitationToHostSerializer(_queryset, many=True)
        return Response(serializers.data)
# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

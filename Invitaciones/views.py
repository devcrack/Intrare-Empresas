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

"""
Usada para listar las invitaciones por usuario.
"""


class InvitationListAdminEmployee(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | IsEmployee,)  # The user logged have to be and admin or an employee
    serializer_class = InvitacionSerializers  # Used for validate and deserializing input, and for serializing output.

    def list(self, request, *args, **kwargs):
        y = self.kwargs['year']
        m = self.kwargs['month']
        d = self.kwargs['day']
        usr = self.request.user
        invitations = None
        if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
            print('IS an ADMINISTRATOR')
            adm_company = Administrador.objects.filter(id_usuario=usr)[0]
            id_company = adm_company.id_empresa
            invitations = Invitacion.objects.filter(id_empresa=id_company, fecha_hora_invitacion__year=y,
                                                    fecha_hora_invitacion__month=m,
                                                    fecha_hora_invitacion__day=d)
        if usr.roll == settings.EMPLEADO:
            print('IS an EMPLOYEE')
            employee = Empleado.objects.filter(id_usuario=usr)[0]
            invitations = Invitacion.objects.filter(id_empleado=employee.id, fecha_hora_invitacion__year=y,
                                                    fecha_hora_invitacion__month=m,
                                                    fecha_hora_invitacion__day=d)
        queryset = self.queryset = invitations
        serializer = InvitationToGuardSerializer(queryset, many=True)
        return Response(serializer.data)


class InvitationListToGuard(viewsets.ModelViewSet):
    permission_classes = (isGuard,)

    def list(self, request, *args, **kwargs):
        qr_code = self.kwargs['qr_code']
        self.queryset = Invitacion.objects.filter(qr_code=qr_code)
        _nReg = len(self.queryset)
        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = InvitationToGuardSerializer(queryset, many=True, context={"request": request})
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationListToSimpleUser(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = Invitacion.objects.filter(id_usuario=self.request.user.id)
        _nReg = len(self.queryset)

        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = InvitationToSimpleUserSerializer(queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin | IsEmployee,)

    def create(self, request, *args, **kwargs):
        usr = self.request.user
        # self.preprocessJson(request.data)
        self.serializer_class = InvitationCreateSerializerAdmin
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            _idCompany = None
            _employee = None
            """
            Reading data from serializer
            """
            _areaId = _serializer.data['areaId']
            _listSecEquip = _serializer.data['secEquip']
            _arraySecEquip = _listSecEquip.split(',')
            _email = _serializer.data['email']
            _cellNumberUser = _serializer.data['cellNumber']
            _dateInv = _serializer.data['dateInv']
            _subject = _serializer.data['subject']
            _vehicle = _serializer.data['vehicle']
            _notes = _serializer.data['notes']
            _companyFrom = _serializer.data['companyFrom']

            if usr.roll == settings.ADMIN:
                print('Logged as Administrator\n')
                _employeeId = _serializer.data['employeeId']
                _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
                _idCompany = _admCompany.id_empresa
                #  Validating Employee
                _errorResponse, _employee = self.validate_employee(_idCompany, _employeeId)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('Logged as Employee\n')
                _employee = Empleado.objects.filter(id_usuario=usr)[0]
                _idCompany = _employee.id_empresa
            print('IDCompany =', _idCompany)
            _errorResponse, _area = self.validate_areas(_idCompany, _areaId)  # Validating if Area exist
            if _area:
                # Validating if Security Equipment Exist
                _securityEqu, _errorResponse = self.validateSecEqu(_arraySecEquip)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)

                # Create Invitation
                _errorResponse, invitation = self.create_invitation(_email, _cellNumberUser, _idCompany, _area,
                                                                    _employee, _dateInv, _subject, _vehicle,
                                                                    _notes, _companyFrom)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if _securityEqu:
                        _errorResponse = self.add_sec_equ_by_inv(_securityEqu, invitation)
            else:
                return Response(data=_errorResponse, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)

        return Response(status=status.HTTP_201_CREATED)


    @classmethod
    def guest_exist(cls, _email):
        user = CustomUser.objects.filter(email=_email)
        if user:
            print('User Exist with email: ', user[0].email)
            return user[0]
        else:
            print('User with this number phone NOT EXIST: ')
            return None

    @classmethod
    def create_invitation(cls, email, cell_phone_number, id_company, id_area, id_employee , date_inv, subject, vehicle,
                          notes, from_company):
        error_response = None
        _mainMsg = 'Bienvenido a Intratre. '
        _msgReg = None
        _link = 'https://first-project-vuejs.herokuapp.com/preregistro/'
        _msgInv = None

        _idUser = cls.guest_exist(email)
        if _idUser is None:
            error_response, _idUser = cls.create_user(email, cell_phone_number)
            if error_response:
                return error_response, None
        print('Data to commit in Invitation\n')
        print('\tCompany Id: ', id_company)
        print('\tArea Id :', id_area)
        print('\tUser Id: ', _idUser)
        print('\tEmploye Id:', id_employee)
        print('\tInvitation Date: ', date_inv)
        print('\tsubject: ', subject)
        print('\tvehicle: ', vehicle)
        print('\tnotes: ', notes)
        print('\tfromCompany: ', from_company)
        nw_invitation = Invitacion(
            id_empresa=id_company,
            id_area=id_area,
            id_usuario=_idUser,
            id_empleado=id_employee,
            fecha_hora_invitacion=date_inv,
            asunto=subject,
            automovil=vehicle,
            notas=notes,
            empresa=from_company,
            )
        try:
            some  = nw_invitation.save()
            print("SOME", some)
        except ValueError:
            error_response = {'Error': 'Can\'t create an Invitation'}
            nw_invitation = None
        if nw_invitation:  # Se ha creado una invitacion satisfactoriamente.
            if _idUser.is_active == True:  # El proceso de notificacion de Invitacion se realiza normalmente
                _msgInv = "Se te ha enviado una invitación, verifica desde tu correo electrónico o la aplicación"
                #  Envio de correo electronico con los datos de la invitacion
                _htmlMessage = cls.render_InvMail(nw_invitation.id_empresa.name, nw_invitation.fecha_hora_invitacion,
                                                  nw_invitation.qr_code)
                _smsResponse = send_sms(_idUser.celular, _msgInv)  # Envio notificacion sms Invitacion.
                send_IntrareEmail(_htmlMessage, _idUser.email)
                log = None
            else: #  Se envia al usuario una notificacion para que realize su preRegistro N VECES
                _msgReg = f'Recibiste una invitación. Para acceder a ella realiza tu Pregistro en: '
                _link = _link + str(_idUser.temporalToken) + '/'
                msg = _mainMsg + _msgReg + _link
                _smsResponse = send_sms(_idUser.celular, msg)  # SMS
                _htmlMessage = cls.render_MsgPregister(_mainMsg, _msgReg, _link)
                send_IntrareEmail(_htmlMessage, _idUser.email)  # EMAIL
            if _smsResponse["messages"][0]["status"] == "0":
                log = 'Mensaje SMS ENVIADO'
            else:
                log = f"Error: {_smsResponse['messages'][0]['error-text']} al enviar SMS"
            print('LOGs SMS!! ')
            print(log)
            print(nw_invitation.id, ' INVITATION CREATED  200_OK')
        return error_response, nw_invitation

    @classmethod
    def render_InvMail(cls, _nameEmpresa, _dateInv, _qrCode):
        html_message = render_to_string('email.html',
                                        {'empresa': _nameEmpresa,
                                         'fecha': _dateInv,
                                         'codigo': _qrCode}
                                       )
        return html_message

    @classmethod
    def render_MsgPregister(cls, _headerMsg, msg, link):
        html_message = render_to_string('nwUserMail.html',
                                        {'headerMsg':_headerMsg,
                                         'msg': msg,
                                         'link': link
                                         })
        return html_message

    @classmethod
    def validate_employee(cls, *args):
        """
        Args:
            args[0]: Id_company.
            args[1]: id_employee.

        Returns:
            tuple:data error message and area if is found it.
        """
        id_company = args[0]
        id_employee = args[1]
        # PREV
        # _first_name = args[1]
        # _last_name = args[2]

        error_response = None
        employee = None
        employee_s = Empleado.objects.filter(id_empresa=id_company, id=id_employee)
        if employee_s:
            print('Employee FOUND! goal!! Goal!!! SUCCESS!!!!')
            employee = employee_s[0]
        else:
            print('Employee NOT FOUND')
            error_response = {'Error': 'The Employee provided do not exist'}
        return error_response, employee

    @classmethod
    def validate_areas(cls, *args):
        """
            Args:
                args[0]: Id_company.
                args[1]: area name.

            Returns:
                tuple:data error message and area if is found it.
        """
        id_company = args[0]
        id_area = args[1]
        area = None
        error_response = None

        area_s = Area.objects.filter(id_empresa=id_company, id=id_area)
        if area_s:
            area = area_s[0]
        else:
            error_response = {'Error': 'No existen areas con el Id proporcionado'}
        return error_response, area

    @classmethod
    def validate_security_equip(cls, name_security_equipment):
        security_equipment = None
        error_response = None
        st_equipments = EquipoSeguridad.objects.filter(nombre=name_security_equipment)
        if st_equipments:
            security_equipment = st_equipments[0]
        else:
            error_response = {'Error': 'No Security Equipment found with data provided'}
        return error_response, security_equipment

    @classmethod
    def create_user(cls, _aemail, cellphone):
        """
        Create a user with minimum requirements data fill.

        Args:
              args[0]: number phone
              args[1]: user name in this case is the number phone too.

        """
        _errorResponse = None
        _email = _aemail
        number_phone = cellphone
        code = token_hex(4)  # Generamos Token para identificar a este usuario y modificarlo posteriormente.
        _password = 'pass'
        #poner token 5 digitos
        nw_user = CustomUser(
             email=_email, celular=number_phone, username=_email, password=_password, temporalToken=code, is_active=False)
        try:
            nw_user.save()
            print(nw_user.id, ' USER CREATED 200_OK')
        except ValueError:
            _errorResponse = {'Error': 'Error in User Create'}
        return _errorResponse, nw_user

    @classmethod
    def validateSecEqu(cls, listSecEq):
        _idSecEqList = []
        for i in listSecEq:
            if i !='':
                print(i)
                _idSecEq = int(i)
                try:
                    _secEqu = EquipoSeguridad.objects.get(id=_idSecEq)
                    _idSecEqList.append(_secEqu)
                except ObjectDoesNotExist:
                    return None, {'Error': 'Error with Security Equipment supplied, please check it'}
        return _idSecEqList, None

    @classmethod
    def add_sec_equ_by_inv(cls, list_equipment_security, inv):
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


class InvitationbyQRCode(generics.ListAPIView):
    serializer_class = InvitationSimpleSerializer

    def get_queryset(self):
        queryset = Invitacion.objects.all()
        self.request.data;
        _qrCode = self.kwargs['qrcode']
        if _qrCode is not None:
            queryset = queryset.filter(qr_code=_qrCode)
        return queryset




# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

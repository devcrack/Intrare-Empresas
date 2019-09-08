# TODO En lugar de nombre de usuario ID de usuario.
#

from hmac import new

from django.db.utils import Error


# Create your views here.
from rest_framework import generics
from rest_framework import viewsets
from datetime import date
from rest_framework.response import Response
from .serializers import *
from Usuarios.permissions import *
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from clx import xms

from string import Template
import os


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
    permission_classes = (IsUser,)

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
            _cellNumberUser = _serializer.data['cellNumber']
            _employeeId = _serializer.data['employeeId']
            _dateInv = _serializer.data['dateInv']
            _subject = _serializer.data['subject']
            _vehicle = _serializer.data['vehicle']
            _notes = _serializer.data['notes']
            _companyFrom = _serializer.data['companyFrom']

            if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
                print('Logged as Administrator\n')
                _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
                _idCompany = _admCompany.id_empresa
                """
                Validating Employee
                """
                _errorResponse, _employee = self.validate_employee(_idCompany, _employeeId)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)
            else:
                print('Logged as Employee\n')
                _employee = Empleado.objects.filter(id_usuario=usr)[0]
                _idCompany = _employee.id_empresa
            """
            Validating if Area exist
            """
            print('IDCompany =', _idCompany)
            _errorResponse, _area = self.validate_areas(_idCompany, _areaId)
            if _area:
                """
                Validating if Security Equipment Exist
                """
                _securityEqu, _errorResponse = self.validateSecEqu(_arraySecEquip)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)
                """
                Create Invitation
                """
                _errorResponse, invitation = self.create_invitation(_cellNumberUser, _idCompany, _area,
                                                                    _employee, _dateInv, _subject, _vehicle,
                                                                    _notes, _companyFrom)
                if _errorResponse:
                    return Response(data=_errorResponse, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # self.send_email(_serializer, invitation, _idCompany)
                    if _securityEqu:
                        _errorResponse = self.add_sec_equ_by_inv(_securityEqu, invitation)
                        # self.send_email(_serializer, invitation, _idCompany)
            else:
                return Response(data=_errorResponse, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)
        self.send_sms(invitation)
        self.send_email(invitation)
        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def send_sms(cls, _inv):
        num = '+52' + _inv.id_usuario.celular
        cliente = xms.Client(
            'c2811649ffa2408eb78ab92d2660a494',
            '06676539d84f46ae842a78b045131e2d',
        )
        batch_params = xms.api.MtBatchTextSmsCreate()
        batch_params.sender = '447537432321'
        batch_params.recipients = {num}
        batch_params.body = 'Intrare, haz recibido una nueva invitacion. Para mas info consulta tu email o desde la app'

        result = cliente.create_batch(batch_params)
        print(result)

    @classmethod
    def send_email(cls, _inv):

        subject = 'Intrare Industrial - Invitación'

        html_message = render_to_string('email.html',
                                        {'empresa': _inv.id_empresa.name,
                                         'fecha': _inv.fecha_hora_invitacion,
                                         'codigo': _inv.qr_code}
                                        )
        message = ''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [_inv.id_usuario.email, ]

        send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, html_message=html_message)



    @classmethod
    def guest_exist(cls, _phone_number):
        user = CustomUser.objects.filter(celular=_phone_number)
        if user:
            print('User Exist with NUMBER PHONE: ', user[0].celular)
            return user[0]
        else:
            print('User with this number phone NOT EXIST: ')
            return None

    @classmethod
    def create_invitation(cls, cell_phone_number, id_company, id_area, id_employee , date_inv, subject, vehicle,
                          notes, from_company):
        """
        Args:
            args[0]: serializer data
            args[1]: id company
            args[2]: id area
            args[3]: id employee
            args[4]: user
        """

        error_response = None
        _idUser = cls.guest_exist(cell_phone_number)
        if _idUser is None:
            error_response, _idUser = cls.create_user(cell_phone_number)
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
            nw_invitation.save()
        except ValueError:
            error_response = {'Error': 'Can\'t create an Invitation'}
            nw_invitation = None

        print(nw_invitation.id, ' INVITATION CREATED  200_OK')
        return error_response, nw_invitation

    @classmethod
    def create_temporal_invitation(cls, *args):
        """
        Args:
            args[0]: serializer data
            args[1]: id company
            args[2]: id area
            args[3]: id employee
            args[4]: cell phone number of recently user created
       """
        data = args[0]
        _id_company = args[1]
        _id_area = args[2]
        _id_employee = args[3]
        cellphone_number_user = args[4]
        date_inv = data['date']
        business = data['business']
        vehicle = data['vehicle']
        notes = data['notes']
        from_company = data['company']
        error_response = None

        tmp_invitation = InvitacionTemporal(
            id_empresa=_id_company, id_area=_id_area,
            id_empleado=_id_employee, celular_invitado=cellphone_number_user,
            fecha_hora_invitacion=date_inv, asunto=business, automovil=vehicle, notas=notes, empresa=from_company
            )
        try:
            tmp_invitation.save()
        except ValueError:
            error_response = {'Error': 'Can\'t create an Invitation'}
            tmp_invitation = None
        print('TEMPORARY INVITATION Created 200_OK')
        return error_response, tmp_invitation

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
    def create_user(cls, *args):
        """
        Create a user with minimum requirements data fill.

        Args:
              args[0]: number phone
              args[1]: user name in this case is the number phone too.

        """
        _errorResponse = None
        number_phone = args[0]
        user = args[0]
        _password = 'pass'
        nw_user = CustomUser(
            celular=number_phone, username=user, password=_password)
        try:
            nw_user.save()
            print(nw_user.id, ' USER CREATED 200_OK')
            return None, nw_user
        except ValueError:
            _errorResponse = {'Error': 'Error in User Create'}
            return _errorResponse, None

    @classmethod
    def EquiposporInvitacion_add(cls, *args):
        security_equipment = args[0]
        inv = args[1]
        error_response = None

        e_s = EquiposporInvitacion(id_equipo_seguridad=security_equipment, id_invitacion=inv)
        try:
            e_s.save()
            print('Equipment by Invitation Created 200_OK')
        except ValueError:
            error_response = {'Error': 'Can\'t create Equipment for invitation'}
        return error_response

    @classmethod
    def EquipoporInvitacionTemporal_Add(cls, *args):
        security_equip = args[0]
        tmp_inv = args[1]
        error_response = None

        e_s = EquipoporInvitacionTemporal(id_equipo_seguridad=security_equip, id_invitacion_temporal=tmp_inv)
        try:
            e_s.save()
            print('Equipment by Invitation Created 200_OK')
        except ValueError:
            error_response = {'Error': 'Can\'t create Equipment for invitation'}
        return error_response

    @classmethod
    def preprocessJson(cls, data):
        print('Printing Json input data\n')
        for key, value in data.items():
            print('Key', key)
            print('Value', value)

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


class MassiveInvitationCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin | IsEmployee,)

    def create(self, request, *args, **kwargs):
        _queVergahay = request.data.get('guests') # En guest llegan todos los numeo de telefono de los invitados
        print(_queVergahay)

# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

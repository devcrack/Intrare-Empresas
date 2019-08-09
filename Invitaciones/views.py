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

from django.template.loader import render_to_string

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

"""
Usada para listar las invitaciones por usuario.
"""
class Invitacion_List(viewsets.ModelViewSet):
    permission_classes = (IsAdmin | IsEmployee,)  # The user logged have to be and admin or an employee
    serializer_class = InvitacionSerializers  # Used for validate and deserializing input, and for serializing output.

    def list(self, request, *args, **kwargs):
        usr = self.request.user
        invitations = None
        if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
            print('IS an ADMINISTRATOR')
            adm_company = Administrador.objects.filter(id_usuario=usr)[0]
            id_company = adm_company.id_empresa
            invitations = Invitacion.objects.filter(id_empresa=id_company)
        if usr.roll == settings.EMPLEADO:
            print('IS an EMPLOYEE')
            employee = Empleado.objects.filter(id_usuario=usr)[0]
            invitations = Invitacion.objects.filter(id_empleado=employee.id)
        queryset = self.queryset = invitations
        serializer = InvitacionSerializers(queryset, many=True)
        return Response(serializer.data)


class InvitationCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin | IsEmployee,)

    def create(self, request, *args, **kwargs):
        usr = self.request.user
        security_equipment = None
        # self.preprocessJson(request.data)
        if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
            print('Logged as Administrator\n')
            self.serializer_class = InvitationCreateSerializerAdmin
            _serializer = self.serializer_class(data=request.data)
            if(_serializer.is_valid()):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)

        """
        When the logged user is an Employee.
        """

        if usr.roll == settings.EMPLEADO:
            print('Logged as Employee\n')

        return Response(status=status.HTTP_200_OK)

    @classmethod
    def send_email(cls, _user, _inv, _compy):

        subject = 'Intrare Industrial - Invitación'

        #html_message = eml.generate(_inv.empresa, _inv.fecha_hora_invitacion, _inv.qr_code)
        html_message = render_to_string('email.html',
                                        {'empresa': _inv.empresa,
                                         'fecha': _inv.fecha_hora_invitacion,
                                         'codigo': _inv.qr_code}
                                        )
        message = ''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [_user.data['email'], ]

        send_mail(subject=subject, message=message, from_email=email_from, recipient_list=recipient_list, html_message=html_message)



    @classmethod
    def guest_exist(cls, _phone_number):
        user = CustomUser.objects.filter(celular=_phone_number)
        if user:
            print('User Exist with NUMBER PHONE: ', user[0].celular)
            return user[0]
        return None

    @classmethod
    def create_invitation(cls, *args):
        """
        Args:
            args[0]: serializer data
            args[1]: id company
            args[2]: id area
            args[3]: id employee
            args[4]: user
        """
        data = args[0]
        id_company = args[1]
        _area = args[2]
        _employee = args[3]
        user = args[4]
        date_inv = data['date']
        business = data['business']
        vehicle = data['vehicle']
        notes = data['notes']
        from_company = data['company']
        error_response = None

        nw_invitation = Invitacion(
            id_empresa=id_company,
            id_area=_area,
            id_usuario=user,
            id_empleado=_employee,
            fecha_hora_invitacion=date_inv,
            asunto=business,
            automovil=vehicle,
            notas=notes,
            empresa=from_company,
            )
        try:
            nw_invitation.save()
        except ValueError:
            error_response = {'Error': 'Can\'t create an Invitation'}
            nw_invitation = None

            qr_code = nw_invitation
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
        id_area= args[1]
        area = None
        error_response = None

        area_s = Area.objects.filter(id_empresa=id_company, id=id_area)
        if area_s:
            area = area_s[0]
            print('Area FOUND: ', area.nombre)
        else:
            error_response = {'Error': 'NO areas found with data provided'}
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
        number_phone = args[0]
        user = args[0]
        _password = 'pass'
        nw_user = CustomUser(
            celular=number_phone, username=user, password=_password)
        try:
            nw_user.save()
            print(nw_user.id, ' USER CREATED 200_OK')
            return nw_user
        except ValueError:
            print('CAN\'T SAVE USER')
            return None

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


# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


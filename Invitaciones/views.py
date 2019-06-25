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
    # serializer_class = InvitacionCreateSerializer

    def create(self, request, *args, **kwargs):
        usr = self.request.user
        security_equipment = None

        if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
            print('Logged as Administrator\n')
            adm_company = Administrador.objects.filter(id_usuario=usr)[0]
            id_company = adm_company.id_empresa
            # usr_employee = CustomUser.objects.filter(n)
            self.serializer_class = InvitationCreateSerializerAdmin
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                _first_name = serializer.data['employee_first_name']  # First name employee provided
                _last_name = serializer.data['employee_last_name']  # Last name employee provided
                area_name = serializer.data['area']
                sec_equip_name = serializer.data['sec_equip']
                """
                Company Data Validations
                """
                error_response, area = self.validate_areas(id_company, area_name)
                if area:  # Validate if AREA Exist
                    if sec_equip_name:  # Validate if security equipment Exist.
                        error_response, security_equipment = self.validate_security_equip(sec_equip_name)
                        if error_response:
                            return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                    error_response, employee = self.validate_employee(id_company, _first_name, _last_name)
                    if employee:  # Validate if EMPLOYEE exist

                        """"
                        Now we can proceed to create an Invitation 
                        """
                        user = self.guest_exist(serializer.data['cell_number'])
                        if user:  # If user guest exist create a normal Invitation.
                            error_response, invitation = self.create_invitation(serializer.data, id_company, area,
                                                                                employee, user)
                            if error_response:
                                return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                if security_equipment:
                                    error_response = self.EquiposporInvitacion_add(security_equipment, invitation)
                                    if error_response:
                                        return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                        else:  # If user not exist create an USER and Temporal Invitation.
                            user = self.create_user(serializer.data['cell_number'])
                            if user:
                                error_response, invitation = self.create_temporal_invitation(serializer.data, id_company, area,
                                                                                             employee, user.celular)
                                if error_response:
                                    return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                    if security_equipment:
                                        error_response = self.EquipoporInvitacionTemporal_Add(security_equipment, invitation)
                                        if error_response:
                                            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                error_response = {'Error': 'Error in User Create'}
                                return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                        print('<SUCCESS>!!!!!!!!!!!!!!!!')
                    else:
                        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_200_OK)

        """
        When the logged user is an Employee.
        """
        if usr.roll == settings.EMPLEADO:
            print('Logged as Employee\n')
            employee = Empleado.objects.filter(id_usuario=usr)[0]
            id_company = employee.id_empresa
            self.serializer_class = InvitationCreateSerializerEmployee
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                sec_equip_name = serializer.data['sec_equip']
                print('Security Equipment', sec_equip_name)
                print('Date ' + str(serializer.data['date']))
                error_response, area = self.validate_areas(id_company, serializer.data['area'])
                if area:  # Validate if AREA exist
                    if sec_equip_name:
                        error_response, security_equipment = self.validate_security_equip(sec_equip_name)
                        if error_response:
                            return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                    user = self.guest_exist(serializer.data['cell_number'])
                    if user: # If user exist just create a normal invitation with the data
                        error_response, invitation = self.create_invitation(serializer.data, id_company, area, employee, user)
                        if error_response:
                            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            if security_equipment:
                                error_response = self.EquiposporInvitacion_add(security_equipment, invitation)
                                if error_response:
                                    return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user = self.create_user(serializer.data['cell_number'])
                        if user:
                            error_response, invitation = self.create_temporal_invitation(serializer.data,
                                                                             id_company, area, employee, user.celular)
                            if error_response:
                                return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                if security_equipment:
                                    error_response = self.EquipoporInvitacionTemporal_Add(security_equipment, invitation)
                                    if error_response:
                                        return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            error_response = {'Error': 'Can\'t  Create User'}
                            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
                    print('<SUCCESS>!!!!!!!!!!!!!!!!')
                else:
                    return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

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
            args[1]: first_name.
            args[2]: last_name.

        Returns:
            tuple:data error message and area if is found it.
        """
        id_company = args[0]
        _first_name = args[1]
        _last_name = args[2]
        error_response = None
        employee = None
        _usr_s = CustomUser.objects.filter(first_name=_first_name, last_name=_last_name)
        if _usr_s:
            usr = _usr_s[0]
            employee_s = Empleado.objects.filter(id_empresa=id_company, id_usuario=usr.id)
            if employee_s:
                print('Employee FOUND! goal!! Goal!!! SUCCESS!!!!')
                employee = employee_s[0]
            else:
                print('Employee NOT FOUND')
                error_response = {'Error': 'The Employee provided do not exist'}
        else:
            print('USER Not Found')
            error_response = {'Error': 'User with provided full name do not exist'}

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
        area_name = args[1]
        area = None
        error_response = None

        area_s = Area.objects.filter(id_empresa=id_company, nombre=area_name)
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
# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


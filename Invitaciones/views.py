from hmac import new

from django.shortcuts import render

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
        print(queryset.values_list())
        print('\n')
        print(type(queryset))
        serializer = InvitacionSerializers(queryset, many=True)
        return Response(serializer.data)


class InvitationCreate(generics.CreateAPIView):
    permission_classes = (IsAdmin | IsEmployee,)
    # serializer_class = InvitacionCreateSerializer

    def create(self, request, *args, **kwargs):
        """

        Args:

        Notes:
            For Empleado user is necesary this data:
                Telefono:
                Correo Electronico:
                Area:
                Fecha y hora de la invitacion
                Asunto:
                Vehiculo:
                Notas:
                Empresa:

        """
        usr = self.request.user
        print('ROLL FROM VIEW', usr.roll)
        #self.serializer_class()
        if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
            print('ROLL->Administrator\n')
            adm_company = Administrador.objects.filter(id_usuario=usr)[0]
            id_company = adm_company.id_empresa
            print('Current Company->', id_company, '\n')
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
                        print('<SUCCESS>!!!!!!!!!!!!!!!!')

                    else:
                        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
        if usr.roll == settings.EMPLEADO:
            print('Employee\n')
            employee = Empleado.objects.filter(id_usuario=usr)[0]
            id_company = employee.id_empresa
            self.serializer_class = InvitationCreateSerializerEmployee
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print('Date ' + str(serializer.data['date']))

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @classmethod
    def guest_exist(cls, serializer):
        cell_phone_number = serializer['cell_number']
        user = CustomUser.objects.filter(celular=cell_phone_number)
        if user:
            return True
        return False

    @classmethod
    def create_invitation(cls, *args):
        data = args[0]
        id_company = args[1]
        _id_area = args[2]
        id_employee = args[3]
        user = args[4]
        date_inv = data['date']
        business = data['business']
        vehicle = data['vehicle']
        notes = data['notes']
        from_company = data['company']
        print('Data')
        print(id_company)
        print(_id_area)
        print(id_employee)
        print(user)
        print(date_inv)
        print(business)
        print(vehicle)
        print(notes)
        print(from_company)



        # nw_inv = Invitacion(


        # nw_inv = Invitacion(
        #     id_empresa=id_company,
        #     id_area=_id_area,
        #     id_empleado=id_employee,
        #     id_usuario=user,
        #
        #     )

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
            print('Current USER: ', usr.id)
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
    def validate_areas(cls,*args):
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



# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


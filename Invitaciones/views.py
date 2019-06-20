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
            print('Administrator\n')
            adm_company = Administrador.objects.filter(id_usuario=usr)[0]
            id_company = adm_company.id_empresa
            print('Current Company->', id_company, '\n')
            # usr_employee = CustomUser.objects.filter(n)
            self.serializer_class = InvitationCreateSerializerAdmin
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                employee_first_name = serializer.data['employee_first_name']  # First name employee provided
                employee_last_name = serializer.data['employee_last_name']  # Last name employee provided
                area_name = serializer.data['area']
                sec_equip_name = serializer.data['sec_equip']

                """
                Company Data Validations
                """
                area_s = Area.objects.filter(id_empresa=id_company, nombre=area_name)
                if area_s:  # VALIDATE AREAS
                    area = area_s[0]

                    sec_equips = EquipoSeguridad.objects.filter(nombre=sec_equip_name)

                    if sec_equips:#Validate

                    print('Current AREA: ', area.nombre)
                    employee_usr_s = CustomUser.objects.filter(first_name=employee_first_name, last_name=employee_last_name)
                    if employee_usr_s:  # USER EXIST
                        _usr_s = employee_usr_s[0]
                        print('Current User:', _usr_s.id, '\n')

                        # Trying get employee in current logged company with current user obtained.
                        employee_s = Empleado.objects.filter(id_empresa=id_company, id_usuario=_usr_s.id)

                        if employee_s:  # EMPLOYEE EXIST
                            get_employee = employee_s[0]
                            print('Employee FOUND! goal!! Goal!!! SUCCESS!!!!')
                            # self.create_invitation(
                            #     serializer.data,
                            #     id_company,
                            #     )
                        else:
                            print('Employee NOT FOUND')
                            error_response = {'Error': 'The Employee provided do not exist'}
                            return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                    else:
                        error_response = {'Error': 'User with provided full name do not exist'}
                        return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)
                else:
                    error_response = {'Error': 'The Area provided do not exist'}
                    return Response(data=error_response, status=status.HTTP_404_NOT_FOUND)

                """
                Guest data validation
                """
                if self.guest_exist(serializer.data):  # Create a normal invitation.
                    print('USER EXIST')
                    # self.create_invitation(
                    #     serializer.data,
                    #     id_company,
                    #     None,
                    #     usr
                    # )
                else:
                    print('USER dont EXIST')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
# How the fuck document p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


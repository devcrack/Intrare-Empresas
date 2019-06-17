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
    serializer_class = InvitacionCreateSerializer

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
        todo:
            * Validar que las areas en el JASON existan.
            * Auto cargar el Id del empleado en el JSON a serializar.
            * Si el Administrador genera la invitacion Validar que existe el empleado al que se asigna en la invitacion.
            * Auto generar el tipo de invitacion de acuerdo a los datos del invitado:
                Es invitacion, o invitacion temporal

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            usr = self.request.user
            tmp_data = request.data.copy()
            print('SERIALIZER DATA\n')
            print(type(serializer.data))

            #self.serializer_class()
            if usr.roll == settings.ADMIN:  # Admin must be show all invitations of  the Company.
                adm_company = Administrador.objects.filter(id_usuario=usr)[0]
                id_company = adm_company.id_empresa
                print('Administrador\n')
            if usr.roll == settings.EMPLEADO:
                employee = Empleado.objects.filter(id_usuario=usr)[0]
                id_company = employee.id_empresa


            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

            #print(tmp_data)

            #number_phone = tmp_data['celular']  # .____.

            #print('Celular', number_phone)  # We have determine if a user exists with this Number
            #user = CustomUser.objects.filter(celular=number_phone)
            #if user:  # If user exist
             #   user = user[0]
                ##self.serializer_class = InvitacionSerializers

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# How the fuck documment p
# https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


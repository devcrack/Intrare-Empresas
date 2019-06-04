from rest_framework import generics
from rest_framework import viewsets
from datetime import date

from .serializers import *
from Usuarios.permissions import *


class Invitacion_List(viewsets.ModelViewSet):
    permission_classes = (is_admin | isEmployee,)  # The user logged have to be and admin or an employee
    serializer_class = InvitacionSerializers  # Used for validate and deserializing input, and for serializing output.

    def list(self, request, *args, **kwargs):
        print('Usuario\n')
        print(request.user)
        # user = request.user
        # today = date.today()
        # print('Today Data\n')
        # print(today)
        # admin_company = Administrador.objects.filter(id_usuario=user)[0]

        # # Here first we have to filter invitation of the current company





    queryset = Invitacion.objects.all()  # Used for return objects from this view.



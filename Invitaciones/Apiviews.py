from rest_framework import generics
from rest_framework import viewsets
from datetime import date
from rest_framework.response import Response
from .serializers import *
from Usuarios.permissions import *


class Invitacion_List(viewsets.ModelViewSet):
    permission_classes = (is_admin | isEmployee,)  # The user logged have to be and admin or an employee
    serializer_class = InvitacionSerializers  # Used for validate and deserializing input, and for serializing output.

    def list(self, request, *args, **kwargs):
        usr = self.request.user
        adm_company = Administrador.objects.filter(id_usuario=usr)[0]
        id_company = adm_company.id_empresa
        inv_this_company = Invitacion.objects.filter(id_empresa=id_company)
        # if is_admin:
        queryset = inv_this_company
        serializer = InvitacionSerializers(queryset, many=True)
        return Response(serializer.data)


        # user = request.user
        # today = date.today()
        # print('Today Data\n')
        # print(today)
        # admin_company = Administrador.objects.filter(id_usuario=user)[0]

        # # Here first we have to filter invitation of the current company





    queryset = Invitacion.objects.all()  # Used for return objects from this view.



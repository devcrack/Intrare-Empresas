from rest_framework.response import Response
from rest_framework import generics, status
from Usuarios.permissions import *
from .serializers import *
from Empresas.models import Vigilante


class BitacoraListCreate(generics.ListCreateAPIView):
    permission_classes = (isEmployee | isGuard,)
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializers

    def create(self, request, *args, **kwargs):
        id_user = self.request.user.id
        vigilante = Vigilante.objects.filter(id_usuario=id_user)[0]
        print(vigilante.id_empresa.id)
        request.data['id_vigilante'] = vigilante.id
        request.data['id_empresa'] = vigilante.id_empresa.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


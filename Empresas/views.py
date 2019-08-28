from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from Empresas.models import Acceso
from Usuarios.permissions import *
from .serializers import AccessCreateSerializer
from .serializers import AccesUpdateSerializer

from Invitaciones.models import Invitacion
from Empresas.models import Vigilante
class AccessCreate(generics.CreateAPIView):
    permission_classes = (isGuard,)

    def create(self, request, *args, **kwargs):
        """
        Creamos una invitacion a partir de los siguientes parametros:
            - id_invitacion: Viene en el cuerpo del json
            - id_vigilante_ent: Se obtiene de la session actual
            - datos_coche: Puede ser Nulo
            - qr_code : No puede ser nulo
        """
        self.serializer_class = AccessCreateSerializer
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            _guard_ent = Vigilante.objects.filter(id_usuario=self.request.user)[0]

            _datos_coche = _serializer.data['datos_coche']
            _qr_code = _serializer.data['qr_code']
            _inv = Invitacion.objects.filter(qr_code=_qr_code)[0]
            self.createAcces(_guard_ent, _inv, _datos_coche, _qr_code)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)
        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def createAcces(cls, _guard_ent, _id_inv, _vehicleData, _qr_code):
        _errorResponse = None
        nwAccess = Acceso(id_vigilante_ent=_guard_ent, id_invitacion=_id_inv, datos_coche=_vehicleData, qr_code=_qr_code)
        nwAccess.save()


class AccessUpdateExitPass(generics.UpdateAPIView):
    queryset = Acceso.objects.all()
    serializer_class = AccesUpdateSerializer
    lookup_field = 'pk'


    def update(self, request, *args, **kwargs):
        """
        JSON
        {
	        "pase_salida":false
        }
        """
        instance = self.get_object()
        instance.pase_salida = request.data.get('pase_salida')
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)
        # serializer = self.get_serializer(instance)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # return Response(serializer.data)

class AccessUpdateData(generics.UpdateAPIView):
    """
    JSON
    {
	    "estado":2,
	    "motivo_no_firma":null,
	    "comentarios_VE":"todo bien"
    }
    """
    queryset = Acceso.objects.all()
    serializer_class = AccesUpdateSerializer
    lookup_field = 'qr_code'
    permission_classes = (isGuard,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        _guard_exit = Vigilante.objects.filter(id_usuario=self.request.user)[0]
        instance.id_vigilante_sal = _guard_exit
        instance.fecha_hora_salida = datetime.now()
        instance.estado = request.data.get('estado')
        instance.motivo_no_firma = request.data.get('motivo_no_firma')
        instance.comentarios_VE = request.data.get('comentarios_VE')
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)

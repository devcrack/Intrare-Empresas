from rest_framework import serializers
from .models import *


class BitacoraSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bitacora
        fields = (
            'id_vigilante',
            'id_caseta',
            'id_empresa',
            'id_empleado',
            'id_area',
            'f_acceso',
            'f_salida',
            'url_foto',
            'nombre',
            'telefono',
            'empresa',
            'notas'
        )

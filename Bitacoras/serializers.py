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


class BitacoraListGuardSerializers(serializers.ModelSerializer):
    areaName =serializers.CharField(source='id_area.nombre')
    hostFirstName = serializers.CharField(source='id_empleado.id_usuario.first_name')
    hostLastName = serializers.CharField(source='id_empleado.id_usuario.last_name')
    f_acceso = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    f_salida = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = Bitacora
        fields = (
            'id',
            'id_caseta',
            'hostFirstName',
            'hostLastName',
            'areaName',
            'f_acceso',
            'f_salida',
            'url_foto',
            'nombre',
            'telefono',
            'empresa',
            'notas'
        )
